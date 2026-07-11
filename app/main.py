from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from .auth import create_access_token, require_admin, verify_password
from .config import Settings, get_settings
from .content_service import get_content_row, save_content_payload
from .db import Base, get_db, get_engine
from .schemas import ContentUpdateRequest, LoginRequest, LoginResponse
from .uploads import save_upload, uploads_dir


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=get_engine())
    uploads_dir()
    yield


app = FastAPI(title="Amani Portfolio API", lifespan=lifespan)

settings = get_settings()
origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=str(uploads_dir())), name="uploads")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/content")
def read_content(db: Session = Depends(get_db)) -> dict:
    row = get_content_row(db)
    return row.payload


@app.put("/api/content")
def update_content(
    body: ContentUpdateRequest,
    db: Session = Depends(get_db),
    _: str = Depends(require_admin),
) -> dict:
    if not isinstance(body.payload, dict) or not body.payload:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="payload must be a non-empty object",
        )
    row = save_content_payload(db, body.payload)
    return row.payload


@app.post("/api/upload")
async def upload_image(
    file: UploadFile = File(...),
    _: str = Depends(require_admin),
) -> dict[str, str]:
    url = await save_upload(file)
    return {"url": url}


@app.post("/api/auth/login", response_model=LoginResponse)
def login(body: LoginRequest, settings: Settings = Depends(get_settings)) -> LoginResponse:
    if body.username != settings.admin_username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    if not verify_password(body.password, settings.resolved_password_hash()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    token = create_access_token(body.username, settings)
    return LoginResponse(access_token=token)
