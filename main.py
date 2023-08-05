import time
import scraper


if __name__ == '__main__':

    print("Welcome in my Web Scraper! Process will start in a moment, please wait...")
    time.sleep(10)

    scraper.scrape_category_urls()
    time.sleep(7)

    scraper.scrape_recipes_urls_from_all_categories()
    time.sleep(7)

    scraper.scrape_details_from_all_recipes()