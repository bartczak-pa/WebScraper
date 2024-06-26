"""Module responsible for scraping new recipes.."""

from scraper import Scraper


class UpdatesScraper(Scraper):
    """Class responsible for parsing new recipes."""

    def __init__(self) -> None:  # noqa: D107
        super().__init__()

    def check_new_categories(self) -> None:
        """Check for new categories."""
        self.categories = self.scrape_categories()

    def scrape_new_recipes(self) -> None:
        """Scrape new recipes from all categories."""
        self.recipes = self.parse_category_urls()
        self.delete_recipes_without_ingredients(self.recipes)
        self.save_data_to_json(self.recipes, "../json_files/recipes_urls.json")
