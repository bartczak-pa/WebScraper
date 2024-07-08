import sched
import time

from scraper.updates_scraper import UpdatesScraper

recipe_updater = sched.scheduler(time.time, time.sleep)


def check_updates() -> None:
    """Run the update function every 24 hours."""
    scraper = UpdatesScraper()
    scraper.check_new_categories()
    scraper.check_new_recipes_from_all_categories()
    recipe_updater.enter(86400, 1, check_updates)
    print("Scraper run complete. Scheduling next run in 24 hours.")  # noqa: T201


recipe_updater.enter(0, 1, check_updates)
recipe_updater.run()
