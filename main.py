import time
from scraper import scrape_category_urls, scrape_recipes_urls_from_all_categories,scrape_details_from_all_recipes
from file_processing import load_data
from utilities import delete_recipes_without_ingredients


if __name__ == '__main__':
    print("Welcome in my Web Scraper! Process will start in a moment, please wait...")
    time.sleep(5)

    # Initial processes scraping all available recipes
    scrape_category_urls()
    category_urls = load_data('json_files/category_urls.json')

    scrape_recipes_urls_from_all_categories(category_urls)
    recipes_urls = load_data('json_files/recipes_urls.json')

    scrape_details_from_all_recipes(recipes_urls)
    all_recipes = load_data('json_files/all_recipes.json')
    delete_recipes_without_ingredients(all_recipes)

    recipes_database = load_data('json_files/recipes_with_ingredients.json')
