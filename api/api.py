"""Api module for the project."""
from pathlib import Path

from fastapi import FastAPI, HTTPException

app = FastAPI()
RECIPES_FILE_PATH = (Path("../json_files/parsed_recipes.json"))


@app.get("/")
def read_root() -> dict:
    """Return default value in API root."""
    return {"App": "Recipes API"}


def check_if_recipes_exists(recipes_file_path: Path) -> Path:
    """Check if file exists and return its path, otherwise raise an exception."""
    if not Path.exists(recipes_file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return recipes_file_path


