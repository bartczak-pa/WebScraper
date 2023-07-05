import requests
from bs4 import BeautifulSoup


# Function scraping category names and their URLs for further processing
def scrape_categories():
    category_list = []

    r = requests.get('https://biancazapatka.com/en/recipe-index/')
    soup = BeautifulSoup(r.content, 'html.parser')

    # Find section containing links to the categories
    categories_div_content = soup.find_all("section",
                                           class_="extendedwopts-hide extendedwopts-mobile widget featured-content "
                                                  "featuredpost"
                                           )

    for category in categories_div_content:

        # Find <h3> element containing category name
        category_name = category.find("h3").text

        # Find <p> elements with class "more-from-category"
        category_links = category.find_all("p", class_="more-from-category")

        # Checks if categories have links/name and extract the href attribute from <a> elements
        if category_links and category_name:
            category_url = category_links[0].find("a").get("href")

            # Saving category name and link to the list
            category_list.append([category_name, category_url])

    # printing scraped categories
    print(f'Scraped {len(category_list)} categories: \n')
    for category in category_list:
        print(category[0])

    return category_list


if __name__ == '__main__':
    pass
