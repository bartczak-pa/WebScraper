"""Module responsible for scraping new recipes.."""
from dataclasses import dataclass
from pathlib import Path

from utilities.file_processing import load_data, save_data_to_json

from .scraper import Scraper


@dataclass
class UpdatesScraper(Scraper):
    """Class responsible for parsing new recipes."""

    def __init__(self) -> None:
        super().__init__({}, {})

    def check_new_categories(self) -> str:
        """Check for new categories."""
        existing_categories: dict = load_data(Path("../json_files/categories.json"))
        new_categories: dict = self.parse_category_urls()
        message: str = ""

        if len(existing_categories) == len(new_categories):
            message = "No new categories have been found."
        elif len(new_categories) > len(existing_categories):
            message = "New categories have been found."
            save_data_to_json(new_categories, "../json_files/categories.json")
        return message

    def scrape_new_recipes(self) -> None:
        """Scrape new recipes from all categories."""
        self.recipes = self.parse_category_urls()
        self.delete_recipes_without_ingredients(self.recipes)
        self.save_data_to_json(self.recipes, "../json_files/recipes_urls.json")
