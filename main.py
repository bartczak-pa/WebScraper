import requests
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


if __name__ == '__main__':
    pass
