import time
import requests

from bs4 import BeautifulSoup
from tqdm import tqdm
from file_processing import save_data_to_json

recipes = {}
PAGE_URL = 'https://biancazapatka.com/en/recipe-index/'


def scrape_category_urls():
    """
    Scrape category names and their URLs for further processing.
    Saves result to category_urls.json file.
    """

    try:
        r = requests.get(PAGE_URL)
        r.raise_for_status()
    except requests.exceptions.ConnectionError as err:
        raise SystemExit(err)

    soup = BeautifulSoup(r.content, 'html.parser')
    categories_div_content = soup.find_all("section", class_="featuredpost")

    if len(categories_div_content) < 0:
        print("It looks like categories div container has not been found")
    else:
        for category in categories_div_content:
            category_name = category.find("h3").text
            category_links = category.find_all("p", class_="more-from-category")

            if category_links and category_name:
                category_url = category_links[0].find("a").get("href")
                recipes[category_name] = {'url': category_url}
        save_data_to_json(recipes, 'json_files/category_urls.json')
        print(f'Scraped titles and URL`s to {len(recipes)} categories \n')


def scrape_recipes_urls(category_name: str, category_url: str):
    """
    Scrape recipes titles and URL`s from one category and saves results to recipes_urls.json file.
    """

    def check_number_of_pages(url: str) -> int:
        """
        Helper function returning amount of pages containing recipes from category
        """

        try:
            request = requests.get(url)
            request.raise_for_status()
        except requests.exceptions.ConnectionError as err:
            raise SystemExit(err)

        pages_num_soup = BeautifulSoup(request.content, "html.parser")

        # Finding element amount of pages to scrape.
        try:
            pages = int(
                str(pages_num_soup.find("li", class_='pagination-next').
                    find_previous("li").
                    find('a').contents[1]).strip())
        except AttributeError:
            pages = 1
        return pages

    category_recipes = {}
    pages_amount = check_number_of_pages(category_url)

    # Loop iterating through all category pages. Use tqdm for displaying inner progress bar in console.
    for page_number in tqdm(range(pages_amount), desc=f'Scraping recipes from {category_name}', position=1,
                            leave=False):

        r = requests.get(f'{category_url}page/{page_number}')
        soup = BeautifulSoup(str(r.content), "html.parser")

        recipe_container = soup.find("div", class_="custom-category-page-wrapper")
        found_recipes = recipe_container.findAll("article")

        recipes_urls = [link.find("a").get("href") for link in found_recipes]
        recipes_titles = [link.find("a").text for link in found_recipes]

        for recipe_title, recipe_url in zip(recipes_titles, recipes_urls):
            category_recipes[recipe_title] = {
                'url': recipe_url
            }

        recipes[category_name].update({'recipes': category_recipes})
        save_data_to_json(recipes, 'json_files/recipes_urls.json')

        # Preventing overloading page with requests
        time.sleep(1)


# Function scraping all recipes from provided category dictionary
def scrape_recipes_urls_from_all_categories():
    """
    Iterates through all categories and scraping URL`s to all recipes.
    Used tqdm for displaying progress bar in console
    """
    for category, values in tqdm(recipes.items(), desc="Scraping recipe URL`s from all categories: ", position=0):
        category_name = category
        category_url = values['url']
        scrape_recipes_urls(category_name, category_url)


def scrape_recipe_details(category: str, recipe_name: str, recipe_url: str):
    """
    Scrape all details from given recipe and saves result in all_recipes.json file.
    """
    details_info = {
        'cook_time': {
            'element': 'span',
            'classes': ['wprm-recipe-cook_time-minutes', 'wprm-recipe-cook_time-hours'],
        },

        'prep_time': {
            'element': 'span',
            'classes': ['wprm-recipe-details-minutes', 'wprm-recipe-details-hours'],
        },

        'total_time': {
            'element': 'span',
            'classes': ['wprm-recipe-total_time-minutes', 'wprm-recipe-total_time-hours'],
        },

        'courses': {
            'element': 'span',
            'classes': ['wprm-recipe-course'],
        },

        'cuisine': {
            'element': 'span',
            'classes': ['wprm-recipe-cuisine'],
        },

        'servings': {
            'element': 'span',
            'classes': ['wprm-recipe-servings'],
        },

        'calories': {
            'element': 'span',
            'classes': ['wprm-recipe-calories'],
        },

        'ingredients': {
            'element': 'ul',
            'classes': ['wprm-recipe-ingredients'],
        },

        'instructions': {
            'element': 'ul',
            'classes': ['wprm-recipe-instructions']
        }

    }
    recipe_content = {}

    r = requests.get(recipe_url)
    soup = BeautifulSoup(r.content, "html.parser")
    recipe_container = soup.find("div", class_="wprm-recipe-container")

    def get_detail(detail_name: str, html_element: str, html_class: str) -> list[str] | dict | str | None:
        """
        Scrape single recipe detail and process them differently for each type
        """
        if recipe_container is not None:
            detail_content = recipe_container.find(html_element, html_class)

            if detail_content is not None:
                if detail_name == 'courses':
                    # TODO clean whitespace from parsed courses
                    courses_list = detail_content.text.split(',')
                    return courses_list

                elif detail_name == 'ingredients':
                    # TODO clean whitespace from parsed ingredients
                    ingredient_names = [ingredient_name.find("span", class_="wprm-recipe-ingredient-name").text
                                        for ingredient_name in detail_content]

                    ingredient_amounts = [ingredient_amount.find("span").text for ingredient_amount in detail_content]
                    ingredients_dict = {}

                    for ingredient_name, amount in zip(ingredient_names, ingredient_amounts):
                        ingredients_dict[ingredient_name] = amount
                    return ingredients_dict

                elif detail_name == 'instructions':
                    instructions_list = [step.text for step in detail_content]
                    return instructions_list

                return detail_content.text
            else:
                return None

    def get_all_details() -> dict:
        """
        Scrape all details from recipe and return dictionary with their values.
        """

        def assign_values(class_order_number: int):
            recipe_content[detail_name] = (
                get_detail(detail_name, detail_values['element'], detail_values['classes'][class_order_number]))

        """
        Some of the recipes have saved times in <span> elements with different classes (minutes/hours). This 
        condition is checking other classes from dictionary in case if script will not be able to scrape primary class
        """
        for detail_name, detail_values in details_info.items():
            assign_values(0)
            if recipe_content[detail_name] is None and len(detail_values['classes']) > 1:
                assign_values(1)

        return recipe_content

    recipes[category]['recipes'][recipe_name].update({'content': get_all_details()})
    save_data_to_json(recipes, 'json_files/all_recipes.json')


def scrape_details_from_all_recipes():
    """
    Iterates through all recipes in dict and scraping their details.
    Used tqdm for displaying progress bar in console
    """
    for category, category_values in tqdm(recipes.items(), desc="Scraping recipes details from all categories: "):
        category_recipes = category_values["recipes"]

        for recipe_name, recipe_values in tqdm(category_recipes.items(),
                                               desc=f'Scraping recipe details from {category}'):
            scrape_recipe_details(category, recipe_name, recipe_values['url'])

            # Preventing overload server with requests
            time.sleep(1)
