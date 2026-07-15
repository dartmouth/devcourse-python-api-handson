# Dartmouth Places

A FastAPI application for sharing useful or interesting places around campus —
quiet study areas, coffee spots, meeting rooms, outdoor locations, and
lesser-known hidden gems. It is the reference implementation for a hands-on
workshop on building RESTful APIs with FastAPI.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended) or plain `pip`

## Installation

```bash
uv sync
```

This installs FastAPI, Uvicorn, SQLModel (Pydantic + SQLAlchemy 2.x).

## Running the API

```bash
uv run fastapi dev
```

Then open the interactive docs:

- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>

