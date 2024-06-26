from scraper.scraper import Scraper
from utilities.file_processing import load_data, save_data_to_json

if __name__ == "__main__":
    """Initialisation of main scraper."""
    scraper = Scraper()
    scraper.categories = load_data("../categories.json")
    scraper.recipes = load_data("../new_recipes.json")

    """Initialisation of updates scraper."""
    updates_scraper = Scraper()

