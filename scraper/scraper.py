"""Module containing functions for scraping recipes from Bianca Zapatka website."""
import logging
import random
import time
from dataclasses import dataclass, field

import requests
from bs4 import BeautifulSoup, ResultSet
from requests import HTTPError, Response
from tqdm import tqdm

from utilities.error_handling import CategoriesDivNotFoundError, UnknownError


@dataclass
class Scraper:
    """Class containing methods for scraping recipes from Bianca Zapatka website."""

    categories: dict
    recipes: dict
    PAGE_URL: str = "https://biancazapatka.com/en/recipe-index/"

    # Number of expected elements in container
    REQUIRED_CONTENT_LENGTH: int = 2

    headers: dict = field(default_factory=lambda: {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ",
    })

    def make_request(self, url: str, retries: int = 3) -> Response | None:
        """Make an HTTP GET request to given URL with retries."""
        for attempt in range(retries):
            try:
                r = requests.get(url, timeout=10, headers=self.headers)
                r.raise_for_status()
            except requests.exceptions.ConnectionError as err:
                if attempt < retries - 1:
                    msg = "Connection error occurred, retrying... (%d/%d)"
                    logging.warning(msg, attempt + 1, retries)
                else:
                    msg = "Connection error occurred after multiple attempts."
                    raise ConnectionError(msg) from err
            except requests.exceptions.HTTPError as err:
                msg = "HTTP error occurred."
                raise HTTPError(msg) from err
            except Exception as err:
                msg = f"Unexpected error occurred: {err}"
                raise UnknownError(msg) from err
            else:
                return r
        return None


    def validate_container_size(self, container: ResultSet) -> None:
        """Check if content exists in container."""
        if len(container) < self.REQUIRED_CONTENT_LENGTH:
            raise CategoriesDivNotFoundError

    def parse_category_urls(self) -> dict[str, dict[str, str]]:
        """Return category names and their URLs."""
        category_urls: dict[str, dict[str, str]] = {}

        r = self.make_request(self.PAGE_URL)
        soup = BeautifulSoup(r.content, "html.parser")
        categories_div_content = soup.find_all("section", class_="featuredpost")
        self.validate_container_size(categories_div_content)

        for category in categories_div_content:
            category_name: str = category.find("h3").text
            category_links: list = category.find_all("p", class_="more-from-category")

            if category_links and category_name:
                category_url: str = category_links[0].find("a").get("href")
                category_urls[category_name] = {"url": category_url}

        logging.info("Found URL's for %d categories.", len(category_urls))
        return category_urls

    def get_pages(self, content: BeautifulSoup) -> int:
        """Return amount of pages from container."""
        try:
            pages = int(
                str(content.find("li", class_="pagination-next").find_previous("li").find("a").contents[1]).strip())
        except AttributeError:
            pages = 1
        return pages

    def check_number_of_pages(self, category_url: str) -> int:
        """Return amount of pages containing recipes from category."""
        r = self.make_request(category_url)
        return self.get_pages(BeautifulSoup(r.content, "html.parser"))


    @staticmethod
    def sleep_for_random_time() -> None:
        """Sleep for random time between 1 and 10 seconds."""
        time.sleep(random.randint(1, 10))  # noqa: S311

    def parse_recipes_urls(self, category_name: str, category_url: str, pages_amount: int) -> dict:
        """Return recipes titles and URL`s from one category."""
        recipes: dict = {}
        recipes_urls_bar = tqdm(total=pages_amount, position=1, desc=category_name, leave=False)

        for page_number in range(1, pages_amount + 1):

            recipes_urls_bar.update(1)
            r = self.make_request(f"{category_url}page/{page_number}")
            soup = BeautifulSoup(str(r.content), "html.parser")

            recipe_container = soup.find("div", class_="custom-category-page-wrapper")
            found_recipes = recipe_container.findAll("article")

            recipes_urls: list = [link.find("a").get("href") for link in found_recipes]
            recipes_titles: list = [link.find("a").text for link in found_recipes]
            # TODO @Pawel: Add code parsing recipes images

            for title, recipe_url in zip(recipes_titles, recipes_urls, strict=False):
                recipes[title] = {"category": category_name, "url": recipe_url}

            if pages_amount > 1:
                Scraper.sleep_for_random_time()

        return recipes

    def parse_recipe_details(self, recipe_url: str) -> dict:  # noqa: C901
        """Return recipe details such as ingredients, steps or cooking time."""
        details_info: dict = {
            "cook_time": {
                "element": "span",
                "classes": ["wprm-recipe-cook_time-minutes", "wprm-recipe-cook_time-hours"],
            },

            "prep_time": {
                "element": "span",
                "classes": ["wprm-recipe-details-minutes", "wprm-recipe-details-hours"],
            },

            "total_time": {
                "element": "span",
                "classes": ["wprm-recipe-total_time-minutes", "wprm-recipe-total_time-hours"],
            },

            "courses": {
                "element": "span",
                "classes": ["wprm-recipe-course"],
            },

            "cuisine": {
                "element": "span",
                "classes": ["wprm-recipe-cuisine"],
            },

            "servings": {
                "element": "span",
                "classes": ["wprm-recipe-servings"],
            },

            "calories": {
                "element": "span",
                "classes": ["wprm-recipe-calories"],
            },

            "ingredients": {
                "element": "ul",
                "classes": ["wprm-recipe-ingredients"],
            },

            "instructions": {
                "element": "ul",
                "classes": ["wprm-recipe-instructions"],
            },

        }
        recipe_content = {}

        r = self.make_request(recipe_url)
        soup = BeautifulSoup(r.content, "html.parser")
        recipe_container = soup.find("div", class_="wprm-recipe-container")

        def get_detail(detail_name: str, html_element: str, html_class: str) -> list[str] | dict | str | None:
            """Return and process single recipe detail."""
            if recipe_container is not None:
                detail_content = recipe_container.find(html_element, html_class)

                if detail_content is not None:
                    if detail_name == "courses":
                        courses_list = [course.strip() for course in detail_content.text.split(",")]
                        [course.strip() for course in courses_list]
                        return courses_list

                    if detail_name == "ingredients":
                        ingredient_names: list = [
                            ingredient_name.find("span", class_="wprm-recipe-ingredient-name").text
                            for ingredient_name in detail_content]

                        ingredient_amounts: list = [ingredient_amount.find("span").text.strip()
                                                    for ingredient_amount in detail_content]

                        ingredients: dict = dict(zip(ingredient_names, ingredient_amounts, strict=False))
                        return ingredients

                    if detail_name == "instructions":
                        instructions: list = [step.text for step in detail_content]
                        return instructions

                    return detail_content.text
            return None

        def get_all_details() -> dict:
            """Return all recipe details."""

            def assign_values(class_order_number: int) -> None:
                recipe_content[detail_name] = (
                    get_detail(detail_name, detail_values["element"], detail_values["classes"][class_order_number]))

            """
            Some of the recipes have saved times in <span> elements with different classes (minutes/hours).
            This condition is checking other classes from dictionary in case if script
            will not be able to scrape primary class
            """
            for detail_name, detail_values in details_info.items():
                assign_values(0)
                if recipe_content[detail_name] is None and len(detail_values["classes"]) > 1:
                    assign_values(1)

            return recipe_content

        return get_all_details()

    def parse_all_recipes_urls(self) -> dict:
        """Return all recipes titles and URL`s from all categories."""
        all_categories_bar = tqdm(total=len(self.categories), position=0, desc="Categories", leave=False)
        tqdm.write("Parsing recipes URLs...")

        for category, values in self.categories.copy().items():
            category_name = category
            category_url = values["url"]
            pages_amount = self.check_number_of_pages(category_url)
            self.recipes.update(self.parse_recipes_urls(category_name, category_url, pages_amount))
            all_categories_bar.update(1)

        return self.recipes
