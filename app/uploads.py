from io import BytesIO
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from PIL import Image, ImageOps, UnidentifiedImageError

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}
ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/pjpeg",
    "image/png",
    "image/gif",
    "image/webp",
    "image/svg+xml",
}
# Browsers (especially Windows) often send these; trust the file extension instead.
PASSTHROUGH_CONTENT_TYPES = {
    "",
    "application/octet-stream",
    "binary/octet-stream",
}
MAX_BYTES = 50 * 1024 * 1024
MAX_EDGE_PX = 2400
JPEG_QUALITY = 85
WEBP_QUALITY = 82


def uploads_dir() -> Path:
    root = Path(__file__).resolve().parent.parent / "uploads"
    root.mkdir(parents=True, exist_ok=True)
    return root


def _normalize_suffix(filename: str) -> str:
    return Path(filename).suffix.lower()


def optimize_raster_image(data: bytes, suffix: str) -> tuple[bytes, str]:
    """Downscale large rasters and recompress. SVG/GIF are left unchanged."""
    if suffix in {".svg", ".gif"}:
        return data, suffix

    try:
        image = Image.open(BytesIO(data))
    except UnidentifiedImageError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not read image file",
        ) from exc

    image = ImageOps.exif_transpose(image)
    width, height = image.size
    longest = max(width, height)
    if longest > MAX_EDGE_PX:
        scale = MAX_EDGE_PX / longest
        image = image.resize(
            (max(1, round(width * scale)), max(1, round(height * scale))),
            Image.Resampling.LANCZOS,
        )

    out = BytesIO()
    if suffix in {".jpg", ".jpeg"}:
        if image.mode in {"RGBA", "LA", "P"}:
            image = image.convert("RGBA")
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1])
            image = background
        elif image.mode != "RGB":
            image = image.convert("RGB")
        image.save(out, format="JPEG", quality=JPEG_QUALITY, optimize=True)
        return out.getvalue(), ".jpg"

    if suffix == ".webp":
        image.save(out, format="WEBP", quality=WEBP_QUALITY, method=6)
        return out.getvalue(), ".webp"

    if suffix == ".png":
        if image.mode not in {"RGB", "RGBA", "L", "LA", "P"}:
            image = image.convert("RGBA")
        image.save(out, format="PNG", optimize=True)
        return out.getvalue(), ".png"

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Unsupported raster type for optimize: {suffix}",
    )


async def save_upload(file: UploadFile) -> str:
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing filename",
        )

    suffix = _normalize_suffix(file.filename)
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {suffix or '(none)'}",
        )

    content_type = (file.content_type or "").split(";")[0].strip().lower()
    if content_type not in PASSTHROUGH_CONTENT_TYPES and content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported content type: {content_type}",
        )

    data = await file.read()
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty file",
        )
    if len(data) > MAX_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File too large (max 50MB)",
        )

    data, suffix = optimize_raster_image(data, suffix)

    name = f"{uuid4().hex}{suffix}"
    dest = uploads_dir() / name
    dest.write_bytes(data)
    return f"/uploads/{name}"
