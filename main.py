"""A script to run the scraper."""

from scraper.scraper import Scraper
from scraper.updates_scraper import UpdatesScraper

if __name__ == "__main__":
    """Initialisation of main and updates scrapers."""
    scraper = Scraper(categories={}, recipes={})
    updates_scraper = UpdatesScraper()
    updates_scraper.check_new_recipes_from_all_categories()



