import time

import scraper
from utilities import delete_recipes_without_ingredients
from file_processing import load_data

if __name__ == '__main__':
    print("Welcome in my Web Scraper! Process will start in a moment, please wait...")
    time.sleep(5)

    scraper.scrape_category_urls()
    scraper.scrape_recipes_urls_from_all_categories()
    scraper.scrape_details_from_all_recipes()

    recipes_to_check = load_data('json_files/all_recipes.json')
    delete_recipes_without_ingredients(recipes_to_check)



