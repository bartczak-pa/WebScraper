"""Module containing functions for scraping recipes from Bianca Zapatka website."""


class Scraper:
    """Class containing methods for scraping recipes from Bianca Zapatka website."""

    def __init__(self: classmethod) -> None:
        self.PAGE_URL: str = "https://biancazapatka.com/en/recipe-index/"
        self.recipes: dict = {}
        self.headers: dict = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ",
        }
