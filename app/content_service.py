import json
from pathlib import Path

from sqlalchemy.orm import Session

from .models import ContentDocument

SEED_PATH = Path(__file__).with_name("seed_data.json")
CONTENT_ROW_ID = 1


def load_seed_payload() -> dict:
    return json.loads(SEED_PATH.read_text(encoding="utf-8"))


def ensure_seeded(db: Session) -> ContentDocument:
    row = db.get(ContentDocument, CONTENT_ROW_ID)
    if row is not None:
        return row

    row = ContentDocument(id=CONTENT_ROW_ID, payload=load_seed_payload())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_content_row(db: Session) -> ContentDocument:
    row = ensure_seeded(db)
    return row


def save_content_payload(db: Session, payload: dict) -> ContentDocument:
    row = ensure_seeded(db)
    row.payload = payload
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
