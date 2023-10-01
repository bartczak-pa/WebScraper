import time

import scraper

if __name__ == '__main__':
    print("Welcome in my Web Scraper! Process will start in a moment, please wait...")
    time.sleep(5)

    scraper.scrape_category_urls()
    scraper.scrape_recipes_urls_from_all_categories()
    scraper.scrape_details_from_all_recipes()
    # TODO function cleaning recipes without ingredients

