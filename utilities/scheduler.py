"""Module responsible for scheduling updates."""
import logging
import signal
import time
from dataclasses import dataclass

import schedule

from scraper.updates_scraper import UpdatesScraper


@dataclass
class UpdatesScheduler:
    """Class responsible for scheduling updates."""

    scraper: UpdatesScraper
    running: bool

    def __init__(self) -> None:
        self.scraper = UpdatesScraper()
        self.running = True

    def check_updates(self) -> None:
        """Check for updates in categories and recipes."""
        self.scraper.check_new_categories()
        self.scraper.check_new_recipes_from_all_categories()
        logging.shutdown()

    def run(self) -> None:
        """Run the scheduler."""
        self.check_updates()
        schedule.every(24).hours.do(self.check_updates)

        def signal_handler(sig: int, frame: object) -> None:  # noqa: ARG001
            self.running = False

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        while True:
            schedule.run_pending()
            time.sleep(10)
