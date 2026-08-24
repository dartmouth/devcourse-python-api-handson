"""FastAPI application entry point for Dartmouth Places."""
from app.routers import places
from app.schemas import HealthResponse

from fastapi import FastAPI

app = FastAPI(
    title="Dartmouth Places",
    description="Share useful or interesting places around campus.",
    version="0.1.0",
)

app.include_router(router=places.router)


@app.get("/health", tags=["health"])
def health() -> HealthResponse:
    """Liveness check. No authentication required."""
    return HealthResponse()


@app.get("/")
def root():
    """A friendly landing message. Visit /docs for the interactive API."""
    return {"message": "Welcome to Dartmouth Places. See /docs for the API."}
