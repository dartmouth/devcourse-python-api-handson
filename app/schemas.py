from typing import Literal

from pydantic import BaseModel
from sqlmodel import Field, SQLModel

class HealthResponse(BaseModel):
    status: Literal["OK"] = "OK"


class Place(SQLModel, table=False):
    id: int
    name: str
    location: str
    description: str
    category: str
    noise_level: str
    has_outlets: bool
    has_wifi: bool
    capacity: int
    is_public: bool
