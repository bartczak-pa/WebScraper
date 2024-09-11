"""Logging configuration for the web scraper."""
import logging
from pathlib import Path


def setup_logging(log_file_path: str = "/app/logs/web_scraper.log") -> None:
    """Set up logging configuration."""
    log_path = Path(log_file_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler(),
        ],
    )
