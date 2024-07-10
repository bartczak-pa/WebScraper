"""A script to run the scraper."""

from scraper.scraper import Scraper
from utilities.scheduler import Scheduler

if __name__ == "__main__":
    """Initialisation of main and updates scrapers."""
    scraper = Scraper(categories={}, recipes={})
    updates = Scheduler()
    updates.run()



