import requests
import time
from bs4 import BeautifulSoup

# Here will  be stored all scraped recipes
all_recipes = {}


# Function scraping category names and their URLs for further processing
def scrape_categories():
    r = requests.get('https://biancazapatka.com/en/recipe-index/')
    soup = BeautifulSoup(r.content, 'html.parser')

    # Find section containing links to the categories
    categories_div_content = soup.find_all("section", class_="featuredpost")

    for category in categories_div_content:

        # Find <h3> element containing category name
        category_name = category.find("h3").text

        # Find <p> elements with class "more-from-category"
        category_links = category.find_all("p", class_="more-from-category")

        # Checks if categories have links/name and extract the href attribute from <a> elements
        if category_links and category_name:
            category_url = category_links[0].find("a").get("href")

            # Saving category name and link to the dictionary
            all_recipes[category_name] = {
                'url': category_url
            }

    # Printing amount of scraped category links
    print(f'Scraped links to {len(all_recipes)} categories')


# Function scraping Recipe titles and URL`s from one category
def scrape_recipes_from_category(category_name, category_url):
    # Variables needed for pagination check loop
    is_have_next_page = True
    page = 1

    # Here will be stored all scraped recipe names and URL`s
    category_recipes = {}

    # Loop checking pagination on the category page
    while is_have_next_page:

        r = requests.get(f'{category_url}page/{page}')
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
        all_recipes[category_name].update({'Recipes': category_recipes})

        # Checking next pagination on category page
        if soup.find("li", class_='pagination-next') is None:
            is_have_next_page = False

        # Preventing overloading page with requests
        time.sleep(2)
        page += 1
        print(f'Changing to page {page} in category {category_name}')


# Function scraping all recipes from provided category dictionary
def scrape_recipes_from_all_categories(recipes_dict):
    for category, values in recipes_dict.items():
        category_name = category
        category_url = values['url']
        scrape_recipes_from_category(category_name, str(category_url))

        print(f'Finished scraping category {category_name}')


if __name__ == '__main__':
    pass
