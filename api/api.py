"""Api module for the project."""
import json
import re
from collections import Counter
from pathlib import Path

from fastapi import FastAPI, HTTPException

app = FastAPI()


def normalize_category_name(category_name: str) -> str:
    """Normalize category names  replacing spaces and special characters with underscores."""
    normalized_name: str = category_name.lower().replace(" ", "_")
    normalized_name = re.sub(r"[^\w\s]", "", normalized_name)
    # Replace double underscores with a single underscore
    return re.sub(r"__+", "_", normalized_name)


def check_if_recipes_exists() -> Path:
    """Check if file exists and return its path, otherwise raise an exception."""
    recipes_file_path = Path("/app/json_files/parsed_recipes.json")
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
    """Return amount of recipes from each normalized category."""
    recipes = decode_recipes()
    normalized_categories = [normalize_category_name(recipe_data["category"].lower()) for recipe_data in recipes.values()]
    return dict(Counter(normalized_categories))


@app.get("/categories/{category_name}")
async def display_category_recipes(category_name: str) -> dict:
    """Return recipes from given category, handling spaces and special characters."""
    normalized_category_name = normalize_category_name(category_name)
    recipes = decode_recipes()
    return {recipe_name: details for recipe_name, details in recipes.items() if
            normalize_category_name(details["category"].lower()) == normalized_category_name}
