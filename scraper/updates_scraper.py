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

        if len(self.existing_categories) == len(new_categories):
            logging.info("No new categories have been found.")
        elif len(new_categories) > len(self.existing_categories):
            logging.info("New categories have been found.")
            save_data_to_json(new_categories, "/app/json_files/categories.json")

    def check_new_recipes_from_category(self, category_name: str, category_url: str) -> None:
        """Check for new recipes in a given category and saves them to the dictionary of existing recipes."""
        new_recipes: dict = self.parse_recipes_urls(category_name, category_url, 1)

        for recipe, values in new_recipes.items():
            if recipe not in self.existing_recipes:
                logging.info("New recipe have been found in category: %s", category_name)
                url: str = values["url"]

                self.existing_recipes[recipe]: dict = {
                    "category": category_name,
                    "url": url,
                    "content": self.parse_recipe_details(url),
                }
                save_data_to_json(self.existing_recipes, "/app/json_files/parsed_recipes.json")
            else:
                # TODO @Pawel: Implement logging only once, not in the loop
                logging.info("No new recipes have been found in category: %s", category_name)

    def check_new_recipes_from_all_categories(self) -> None:
        """Check for new recipes in all categories and saves them in dictionary of existing recipes."""
        for category, values in self.existing_categories.items():
            self.check_new_recipes_from_category(category, values["url"])
