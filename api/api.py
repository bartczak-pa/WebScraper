"""Api module for the project."""
import json
from collections import Counter
from pathlib import Path

from fastapi import FastAPI, HTTPException

app = FastAPI()


def check_if_recipes_exists() -> Path:
    """Check if file exists and return its path, otherwise raise an exception."""
    recipes_file_path = Path("../json_files/parsed_recipes.json")
    if not Path.exists(recipes_file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return recipes_file_path


def decode_recipes() -> dict:
    """Decode recipes from JSON file."""
    try:
        with Path.open(check_if_recipes_exists()) as file:
            recipes = json.load(file)
    except json.JSONDecodeError as err:
        raise HTTPException(status_code=500, detail="Error reading JSON file") from err
    return recipes


@app.get("/")
def read_root() -> dict:
    """Return default value in API root."""
    return {"App": "Recipes API"}


@app.get("/categories")
async def display_amount_of_recipes_per_category() -> dict:
    """Return amount of recipes from each category."""
    recipes = decode_recipes()
    categories: list = [recipe_data["category"].lower() for recipe_data in recipes.values()]
    return dict(Counter(categories))



