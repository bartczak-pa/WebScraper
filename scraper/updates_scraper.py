"""Module responsible for scraping new recipes."""
import logging
from dataclasses import dataclass
from pathlib import Path

from utilities.file_processing import load_data, save_data_to_json

from .scraper import Scraper

#Configure logging
log_file_path = Path("logs/updates_scraper.log")
log_file_path.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler(),
    ],
)

@dataclass
class UpdatesScraper(Scraper):
    """Class responsible for parsing new recipes."""

    def __init__(self) -> None:
        super().__init__({}, {})
        self.existing_categories: dict = load_data(Path("/app/json_files/categories.json"))
        self.existing_recipes: dict = load_data(Path("/app/json_files/parsed_recipes.json"))

    def check_new_categories(self) -> None:
        """Check for new categories and compare them with dictionary of existing categories."""
        new_categories: dict = self.parse_category_urls()
        if new_categories_found := {
            cat: new_categories[cat]
            for cat in new_categories
            if cat not in self.existing_categories
        }:
            logging.info("New categories have been found: %s", ", ".join(new_categories_found.keys()))
            save_data_to_json(new_categories, "/app/json_files/categories.json")
        else:
            logging.info("No new categories have been found.")

    def check_new_recipes_from_category(self, category_name: str, category_url: str) -> None:
        """Check for new recipes in a given category and saves them to the dictionary of existing recipes."""
        new_recipes: dict = self.parse_recipes_urls(category_name, category_url, 1)

        if new_recipes_found := {
            recipe: values
            for recipe, values in new_recipes.items()
            if recipe not in self.existing_recipes
        }:
            logging.info("New recipes have been found in %s: %s", category_name, ", ".join(new_recipes_found.keys()))
            # Update existing recipes with new ones
            for recipe, values in new_recipes_found.items():
                url: str = values["url"]
                self.existing_recipes[recipe] = {
                    "category": category_name,
                    "url": url,
                    "content": self.parse_recipe_details(url),
                }
            save_data_to_json(self.existing_recipes, "/app/json_files/parsed_recipes.json")
        else:
            logging.info("No new recipes have been found in %s.", category_name)


    def check_new_recipes_from_all_categories(self) -> None:
        """Check for new recipes in all categories and saves them in dictionary of existing recipes."""
        for category, values in self.existing_categories.items():
            self.check_new_recipes_from_category(category, values["url"])
