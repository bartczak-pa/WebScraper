"""Module responsible for scheduling updates."""
import time
from dataclasses import dataclass

import schedule

from scraper.updates_scraper import UpdatesScraper


@dataclass
class UpdatesScheduler:
    """Class responsible for scheduling updates."""

    def __init__(self) -> None:
        self.scraper = UpdatesScraper()

    def check_updates(self) -> None:
        """Check for updates in categories and recipes."""
        self.scraper.check_new_categories()
        self.scraper.check_new_recipes_from_all_categories()

    def run(self) -> None:
        """Run the scheduler."""
        self.check_updates()
        schedule.every(24).hours.do(self.check_updates)

        while True:
            schedule.run_pending()
            time.sleep(1)
