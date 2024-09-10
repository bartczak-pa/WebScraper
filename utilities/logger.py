"""Logging configuration for the web scraper."""
import logging
from pathlib import Path


def setup_logging() -> None:
    """Set up logging configuration."""
    log_file_path = Path("logs/web_scraper.log")
    log_file_path.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler(),
        ],
    )
