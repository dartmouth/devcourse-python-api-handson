"""Place routes."""

from app.schemas import Place

from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/places", tags=["places"])

_PLACES: list[Place] = [
    Place(
        id=1,
        name="Quiet corner in Baker-Berry",
        location="Baker-Berry Library",
        description="A hushed nook on the upper floor, perfect for deep focus.",
        category="study",
        noise_level="silent",
        has_outlets=True,
        has_wifi=True,
        capacity=4,
        is_public=True,
    ),
    Place(
        id=2,
        name="Collis Patio",
        location="Collis Center",
        description="Outdoor tables with a view of the Green; lively at lunchtime.",
        category="coffee",
        noise_level="lively",
        has_outlets=False,
        has_wifi=True,
        capacity=30,
        is_public=True,
    ),
    Place(
        id=3,
        name="Life Sciences Center Atrium",
        location="Life Sciences Center",
        description="Bright, airy atrium with plenty of seating and natural light.",
        category="meeting",
        noise_level="moderate",
        has_outlets=True,
        has_wifi=True,
        capacity=60,
        is_public=True,
    ),
]


@router.get("")
def list_places() -> list[Place]:
    """Return all places."""
    return _PLACES


@router.get("/{place_id}")
def get_place(place_id: int) -> Place:
    """Return a single place by id, or 404 if it does not exist."""
    for place in _PLACES:
        if place.id == place_id:
            return place
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Place not found",
    )
