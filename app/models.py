"""SQLModel ORM models — the ``table=True`` classes."""

from datetime import datetime, timezone

from sqlmodel import Field, SQLModel

from app.schemas import Category, NoiseLevel


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Place(SQLModel, table=True):
    """A useful or interesting place around campus."""

    id: int | None = Field(default=None, primary_key=True)
    name: str
    location: str
    description: str
    category: Category
    noise_level: NoiseLevel | None = Field(default=None)
    has_outlets: bool = Field(default=False)
    has_wifi: bool = Field(default=True)
    capacity: int | None = Field(default=None)
    is_public: bool = Field(default=True)

    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)
