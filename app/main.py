"""FastAPI application entry point for Dartmouth Places."""
from contextlib import asynccontextmanager

from app.database import create_db_and_tables
from app.middleware.auth import verify_bearer_token
from app.routers import places
from app.schemas import HealthResponse

from fastapi import FastAPI, Depends

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup. 
    create_db_and_tables()
    yield


app = FastAPI(
    title="Dartmouth Places",
    description="Share useful or interesting places around campus.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(
    router=places.router,
    # dependencies=[Depends(verify_bearer_token)],  # Protect the entire router
)


@app.get("/health", tags=["health"])
def health() -> HealthResponse:
    """Liveness check. No authentication required."""
    return HealthResponse()


@app.get("/")
def root():
    """A friendly landing message. Visit /docs for the interactive API."""
    return {"message": "Welcome to Dartmouth Places. See /docs for the API."}
