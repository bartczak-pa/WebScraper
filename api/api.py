"""Api module for the project."""
from pathlib import Path

from fastapi import FastAPI, HTTPException

app = FastAPI()
FILES_PATH = (Path("../json_files/"))


@app.get("/")
def read_root() -> dict:
    """Return default value in API root."""
    return {"App": "Recipes API"}


def check_if_file_exists(file_name: str) -> Path:
    """Check if file exists and return its path, otherwise raise an exception."""
    file_path = FILES_PATH / file_name

    if not Path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return file_path

