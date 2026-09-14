"""Place routes."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlmodel import Session, select

from app.database import get_session
from app.models import Place
from app.schemas import Category, NoiseLevel, PlaceCreate, PlaceResponse, PlaceUpdate

router = APIRouter(prefix="/places", tags=["places"])


@router.get("", response_model=list[PlaceResponse])
def list_places(
    session: Session = Depends(get_session),
    category: Category | None = None,
    noise_level: NoiseLevel | None = None,
    location: str | None = None,
    has_outlets: bool | None = None,
    has_wifi: bool | None = None,
    min_capacity: int | None = Query(default=None, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[Place]:
    """Return public places, with optional filters and pagination.

    Only public places are returned. ``location`` is a case-insensitive
    partial match; the other filters are exact. ``min_capacity`` matches places
    whose capacity is at least the given value.
    """
    statement = select(Place).where(Place.is_public == True)  # noqa: E712

    if category is not None:
        statement = statement.where(Place.category == category)
    if noise_level is not None:
        statement = statement.where(Place.noise_level == noise_level)
    if location is not None:
        statement = statement.where(Place.location == location)
    if has_outlets is not None:
        statement = statement.where(Place.has_outlets == has_outlets)
    if has_wifi is not None:
        statement = statement.where(Place.has_wifi == has_wifi)
    if min_capacity is not None:
        statement = statement.where(Place.capacity >= min_capacity)

    statement = statement.order_by(Place.id).offset(offset).limit(limit)
    return list(session.exec(statement).all())


@router.get("/{place_id}", response_model=PlaceResponse)
def get_place(place_id: int, session: Session = Depends(get_session)) -> Place:
    """Return a single place, or 404."""

    place = session.get(Place, place_id)
    if place is None or not place.is_public:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Place not found",
        )
    return place


@router.post("", response_model=PlaceResponse, status_code=status.HTTP_201_CREATED)
def create_place(
    payload: PlaceCreate,
    session: Session = Depends(get_session),
) -> Place:
    """Create a place."""

    now = datetime.now(timezone.utc)
    place = Place(
        **payload.model_dump(),
        created_at=now,
        updated_at=now,
    )
    session.add(place)
    session.commit()
    session.refresh(place)
    return place


@router.patch("/{place_id}", response_model=PlaceResponse)
def update_place(
    place_id: int,
    payload: PlaceUpdate,
    session: Session = Depends(get_session),
) -> Place:
    """Partially update a place.

    Only the fields the client supplies are changed. Returns 404 if missing.
    """

    place = session.get(Place, place_id)
    if place is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Place not found",
        )
    # exclude_unset ensures we only touch fields the client actually sent.
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(place, field, value)
    place.updated_at = datetime.now(timezone.utc)
    session.add(place)
    session.commit()
    session.refresh(place)
    return place


@router.delete("/{place_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_place(
    place_id: int,
    session: Session = Depends(get_session),
) -> Response:
    """Delete a place.

    Returns 404 if missing.
    """
    place = session.get(Place, place_id)
    if place is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Place not found",
        )
    session.delete(place)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
