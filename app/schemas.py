from typing import Literal
from enum import Enum

from pydantic import BaseModel, Field
from datetime import datetime

class HealthResponse(BaseModel):
    status: Literal["OK"] = "OK"


class Category(str, Enum):
    """The kind of place being shared."""

    study = "study"
    coffee = "coffee"
    meeting = "meeting"
    outdoor = "outdoor"
    food = "food"
    hidden_gem = "hidden_gem"
    other = "other"


class NoiseLevel(str, Enum):
    """How loud a place typically is."""

    silent = "silent"
    quiet = "quiet"
    moderate = "moderate"
    lively = "lively"


class PlaceCreate(BaseModel):
    """Fields a client may supply when creating a place."""

    name: str = Field(min_length=1, max_length=100)
    location: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1, max_length=1000)
    category: Category
    noise_level: NoiseLevel | None = None
    has_outlets: bool = False
    has_wifi: bool = True
    capacity: int | None = Field(default=None, gt=0)
    is_public: bool = True


class PlaceResponse(BaseModel):
    """What the API returns for a place."""

    id: int
    name: str
    location: str
    description: str
    category: Category
    noise_level: NoiseLevel | None
    has_outlets: bool
    has_wifi: bool
    capacity: int | None
    is_public: bool
    created_at: datetime
    updated_at: datetime


class PlaceUpdate(BaseModel):
    """Partial update: every field is optional.

    Only the fields a client actually supplies are changed.
    """

    name: str | None = Field(default=None, min_length=1, max_length=100)
    location: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, min_length=1, max_length=1000)
    category: Category | None = None
    noise_level: NoiseLevel | None = None
    has_outlets: bool | None = None
    has_wifi: bool | None = None
    capacity: int | None = Field(default=None, gt=0)
    is_public: bool | None = None
