import time
import requests

from bs4 import BeautifulSoup
from tqdm import tqdm

recipes = {}


# Function scraping category names and their URLs for further processing
def scrape_category_urls():
    try:
        r = requests.get('https://biancazapatka.com/en/recipe-index/')
        r.raise_for_status()
    except requests.exceptions.ConnectionError as err:
        raise SystemExit(err)

    soup = BeautifulSoup(r.content, 'html.parser')

    # Find section containing links to the categories
    categories_div_content = soup.find_all("section", class_="featuredpost")

    # Loop checking if the content with categories have been found.
    if len(categories_div_content) < 0:
        print("It looks like categories div container has not been found")
    else:
        for category in categories_div_content:

            # Find <h3> element containing category name
            category_name = category.find("h3").text

            # Find <p> elements with class "more-from-category"
            category_links = category.find_all("p", class_="more-from-category")

            # Checks if categories have links/name and extract the href attribute from <a> elements
            if category_links and category_name:
                category_url = category_links[0].find("a").get("href")

                # Saving category name and link to the dictionary
                recipes[category_name] = {
                    'url': category_url
                }

        print(f'Scraped titles and URL`s to {len(recipes)} categories \n')


# Function scraping Recipe titles and URL`s from one category
def scrape_recipes_urls(category_name, category_url):
    # Helper function returning amount of pages containing recipes from category
    def check_number_of_pages(url):

        try:
            request = requests.get(url)
            request.raise_for_status()
        except requests.exceptions.ConnectionError as err:
            raise SystemExit(err)

        pages_num_soup = BeautifulSoup(request.content, "html.parser")

        try:
            pag_amount = int(
                str(pages_num_soup.find("li", class_='pagination-next').find_previous("li").find('a').contents[
                        -1]).strip())
        except AttributeError:
            pag_amount = 1

        return pag_amount

    # In this variable will be stored amount of pages containing recipes from category
    pages_amount = check_number_of_pages(category_url)

    # Here will be stored all scraped recipe names and URL`s
    category_recipes = {}

    # Loop iterating through all category pages. Use tqdm for displaying inner progress bar in console.
    for page_number in tqdm(range(pages_amount), desc=f'Scraping recipes from {category_name}', position=1,
                            leave=False):

        r = requests.get(f'{category_url}page/{page_number}')
        soup = BeautifulSoup(str(r.content), "html.parser")

        # Find <div> elements with class "custom-category-page-wrapper"
        recipe_container = soup.find("div", class_="custom-category-page-wrapper")

        # Find <article> elements containing links to recipes
        found_recipes = recipe_container.findAll("article")

        # Extract the href attribute from <a> elements
        recipes_urls = [link.find("a").get("href") for link in found_recipes]

        # Extract the recipe title from <a> elements
        recipes_titles = [link.find("a").text for link in found_recipes]

        # Adding recipe titles and url`s to dictionary
        for recipe_title, recipe_url in zip(recipes_titles, recipes_urls):
            category_recipes[recipe_title] = {
                'url': recipe_url
            }

        # Updating main dictionary with scraped recipe names and urls
        recipes[category_name].update({'Recipes': category_recipes})

        # Preventing overloading page with requests
        time.sleep(2)


# Function scraping all recipes from provided category dictionary
def scrape_recipes_urls_from_all_categories():
    """
    This loop iterates through all categories and scraping URLs to all recipes.

    Used tqdm for displaying progress bar in console

    """
    for category, values in tqdm(recipes.items(), desc="Scraping recipe URL`s from all categories: ", position=0):
        category_name = category
        category_url = values['url']
        scrape_recipes_urls(category_name, category_url)


def scrape_recipe_details(category, recipe_name, recipe_url):
    r = requests.get(recipe_url)
    soup = BeautifulSoup(r.content, "html.parser")

    # Find <div> element with class "wprm-recipe-container"
    recipe_container = soup.find("div", class_="wprm-recipe-container")

    """As some recipe pages are general articles and don't include times or ingredients, we have to check existence of
    specific fields. Functions below are responsible for scraping those details. Some of recipes have saved times in
    <span> elements with different classes (minutes/hours)
    """

    def get_cook_time():
        try:
            # Find <span> element containing cook time in minutes
            cook_time_content = recipe_container.find('span', class_='wprm-recipe-cook_time-minutes')
            return cook_time_content.text
        except AttributeError:
            try:
                # Find <span> element containing recipe time in hours
                cook_time_content = recipe_container.find('span', class_='wprm-recipe-cook_time-hours')
                return cook_time_content.text
            except AttributeError:
                cook_time_content = 0
                return cook_time_content

    def get_prep_time():
        try:
            # Find <span> element containing prep time in minutes
            prep_time_content = recipe_container.find('span', class_='wprm-recipe-details-minutes')
            return prep_time_content.text

        except AttributeError:
            try:
                # Find <span> element containing prep time in hours
                prep_time_content = recipe_container.find('span', class_='wprm-recipe-details-hours')
                return prep_time_content.text

            except AttributeError:
                prep_time_content = 0
                return prep_time_content

    def get_total_time():
        try:
            # Find <span> element containing total time in minutes
            total_time_content = recipe_container.find('span', class_='wprm-recipe-total_time-minutes')
            return total_time_content.text

        except AttributeError:
            try:
                # Find <span> element containing prep time in hours
                total_time_content = recipe_container.find('span', class_='wprm-recipe-total_time-hours')
                return total_time_content.text

            except AttributeError:
                total_time_content = 0
                return total_time_content

    def get_courses():
        try:
            # Find <span> element containing recipe courses
            course = recipe_container.find("span", class_="wprm-recipe-course")
            courses = course.text.split(',')
            return courses

        except AttributeError:
            courses = ''
            return courses

    def get_cuisine():
        try:
            # Find <span> element containing recipe cuisine
            cuisine_content = recipe_container.find('span', class_='wprm-recipe-cuisine')
            return cuisine_content.text

        except AttributeError:
            cuisine_content = ''
            return cuisine_content

    def get_servings():
        try:
            # Find <span> element containing recipe servings
            servings_content = recipe_container.find("span", class_="wprm-recipe-servings")
            return servings_content.text

        except AttributeError:
            servings_content = 0
            return servings_content

    def get_calories():
        try:
            # Find <span> element containing recipe calories
            calories_content = recipe_container.find('span', class_="wprm-recipe-calories")
            return calories_content.text

        except AttributeError:
            calories_content = 0
            return calories_content

    def get_ingredients():
        try:
            # Find <ul> element containing recipe ingredients
            ingredients_container = recipe_container.find("ul", class_="wprm-recipe-ingredients")

            # Extract ingredients and amounts to the lists
            ingredient_names = [ingredient_name.find("span", class_="wprm-recipe-ingredient-name").text for
                                ingredient_name in
                                ingredients_container]

            ingredient_amounts = [ingredient_amount.find("span").text for ingredient_amount in ingredients_container]

            # Here will be stored data representing each ingredient and its value
            ingredients_dict = {}

            # Add ingredients names and amounts to dict
            for ingredient_name, amount in zip(ingredient_names, ingredient_amounts):
                ingredients_dict[ingredient_name] = amount

            return ingredients_dict

        except AttributeError:
            ingredients_dict = {}
            return ingredients_dict

    def get_instructions():
        try:

            # Find <ul> element containing instructions
            instructions_container = soup.find("ul", class_="wprm-recipe-instructions")

            # Adding instructions to the list
            instructions_list = [step.text for step in instructions_container]
            return instructions_list

        except AttributeError and TypeError:
            return []

    # Dictionary with data for update main dictionary
    recipe_content = {
        'prep_time': get_prep_time(),
        'cook_time': get_cook_time(),
        'total_time': get_total_time(),
        'courses': get_courses(),
        'cuisine': get_cuisine(),
        'servings': get_servings(),
        'calories': get_calories(),
        'ingredients': get_ingredients(),
        'instructions': get_instructions()
    }

    # Updating main dictionary with scraped recipe names and urls
    recipes[category]['Recipes'][recipe_name].update({'Content': recipe_content})


# Function scraping all recipes details from provided dictionary
def scrape_details_from_all_recipes():
    """
    This loop iterates through all recipes in dict and scraping their details.

    Used tqdm for displaying progress bar in console
    """
    for category, category_values in tqdm(recipes.items(), desc="Scraping recipes details from all categories: "):
        category_recipes = category_values["Recipes"]

        for recipe_name, recipe_values in tqdm(category_recipes.items(),
                                               desc=f'Scraping recipe details from {category}'):
            scrape_recipe_details(category, recipe_name, recipe_values['url'])

            # Preventing overload server with requests
            time.sleep(2)
