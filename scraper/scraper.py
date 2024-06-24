"""Module containing functions for scraping recipes from Bianca Zapatka website."""
import requests
from bs4 import BeautifulSoup
from requests import HTTPError

from scraper.error_handling import CategoriesDivNotFoundError, UnknownError


class Scraper:
    """Class containing methods for scraping recipes from Bianca Zapatka website."""

    def __init__(self: classmethod) -> None:
        """Initialize a scraper with base URL, headers, and empty dictionary for recipes."""
        self.PAGE_URL: str = "https://biancazapatka.com/en/recipe-index/"
        self.recipes: dict = {}
        self.headers: dict = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ",
        }

    def parse_category_urls(self) -> dict[str, dict[str, str]]:
        """Return category names and their URLs."""
        category_urls: dict[str, dict[str, str]] = {}

        try:
            r = requests.get(self.PAGE_URL, timeout=10, headers=self.headers)
            r.raise_for_status()

        except requests.exceptions.ConnectionError as err:
            message: str = "Connection error occurred."
            raise ConnectionError(message) from err
        except requests.exceptions.HTTPError as err:
            message: str = "HTTP error occurred."
            raise HTTPError(message) from err
        except Exception as err:
            message: str = "Unexpected error occurred: " + str(err)
            raise UnknownError(message) from err

        else:
            soup = BeautifulSoup(r.content, "html.parser")
            categories_div_content = soup.find_all("section", class_="featuredpost")

            try:
                # Try to access the second element in the list
                categories_div_content[1]
            except IndexError as err:
                raise CategoriesDivNotFoundError from err

            else:
                for category in categories_div_content:
                    category_name: str = category.find("h3").text
                    category_links: list = category.find_all("p", class_="more-from-category")

                    if category_links and category_name:
                        category_url: str = category_links[0].find("a").get("href")
                        category_urls[category_name] = {"url": category_url}
            return category_urls

    @staticmethod
    def check_number_of_pages(category_url: str) -> int:
        """Return  amount of pages containing recipes from category."""
        try:
            r = requests.get(category_url, timeout=10)
            r.raise_for_status()

        except requests.exceptions.ConnectionError as err:
            message: str = "Connection error occurred."
            raise ConnectionError(message) from err
        except requests.exceptions.HTTPError as err:
            message: str = "HTTP error occurred."
            raise HTTPError(message) from err
        except Exception as err:
            message: str = "Unexpected error occurred: " + str(err)
            raise UnknownError(message) from err
        else:
            pages_num_soup = BeautifulSoup(r.content, "html.parser")
            try:
                pages = int(
                    str(pages_num_soup.find("li", class_="pagination-next").
                        find_previous("li").
                        find("a").contents[1]).strip())
            except AttributeError:
                pages = 1
            return pages
