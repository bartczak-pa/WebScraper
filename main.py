"""A script to run the scraper."""
from pathlib import Path

from scraper.scraper import Scraper
from utilities.file_processing import load_data
from utilities.scheduler import UpdatesScheduler

if __name__ == "__main__":
    """Initialisation of main and updates scrapers."""
    scraper = Scraper(categories=load_data(Path("json_files/categories.json")), recipes={})
    #updates = UpdatesScheduler()
    #updates.run()
    scraper.parse_all_recipes_urls()




