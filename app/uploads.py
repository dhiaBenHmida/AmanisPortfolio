from io import BytesIO
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from PIL import Image, ImageFile, ImageOps, UnidentifiedImageError

# Oversized design exports can exceed Pillow's default bomb threshold.
Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True

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
MAX_EDGE_PX = 1600
JPEG_QUALITY = 80
WEBP_QUALITY = 80
# Re-encode large PNGs to JPEG the same way the browser upload path does.
FORCE_JPEG_BYTES = 1 * 1024 * 1024


def uploads_dir() -> Path:
    root = Path(__file__).resolve().parent.parent / "uploads"
    root.mkdir(parents=True, exist_ok=True)
    return root


def _normalize_suffix(filename: str) -> str:
    return Path(filename).suffix.lower()


def _to_rgb(image: Image.Image) -> Image.Image:
    if image.mode in {"RGBA", "LA"}:
        background = Image.new("RGB", image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[-1])
        return background
    if image.mode == "P":
        converted = image.convert("RGBA")
        background = Image.new("RGB", converted.size, (255, 255, 255))
        background.paste(converted, mask=converted.split()[-1])
        return background
    if image.mode != "RGB":
        return image.convert("RGB")
    return image


def optimize_raster_image(data: bytes, suffix: str) -> tuple[bytes, str]:
    """Downscale large rasters and recompress. SVG/GIF are left unchanged."""
    if suffix in {".svg", ".gif"}:
        return data, suffix

    try:
        image = Image.open(BytesIO(data))
        image.load()
    except UnidentifiedImageError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not read image file",
        ) from exc

    image = ImageOps.exif_transpose(image)
    width, height = image.size
    longest = max(width, height)
    if longest > MAX_EDGE_PX:
        # thumbnail mutates in place and is lighter on huge exports
        image.thumbnail((MAX_EDGE_PX, MAX_EDGE_PX), Image.Resampling.LANCZOS)

    out = BytesIO()
    as_jpeg = suffix in {".jpg", ".jpeg"} or len(data) >= FORCE_JPEG_BYTES or longest > MAX_EDGE_PX

    if suffix == ".webp" and not as_jpeg:
        image.save(out, format="WEBP", quality=WEBP_QUALITY, method=6)
        return out.getvalue(), ".webp"

    if suffix == ".png" and not as_jpeg:
        if image.mode not in {"RGB", "RGBA", "L", "LA", "P"}:
            image = image.convert("RGBA")
        image.save(out, format="PNG", optimize=True)
        return out.getvalue(), ".png"

    if as_jpeg or suffix in {".jpg", ".jpeg"}:
        image = _to_rgb(image)
        image.save(out, format="JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
        return out.getvalue(), ".jpg"

    if suffix == ".webp":
        image.save(out, format="WEBP", quality=WEBP_QUALITY, method=6)
        return out.getvalue(), ".webp"

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
