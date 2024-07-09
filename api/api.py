"""Api module for the project."""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root() -> dict:
    """Return default value in API root."""
    return {"App": "Recipes API"}

