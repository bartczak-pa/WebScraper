from file_processing import save_data_to_json
from scraper import scrape_recipes_urls


def delete_recipes_without_ingredients(recipes_input_data: dict):
    """
    Deletes recipes from input dictionary and saves results to correct_recipes.json file.
    """

    def find_recipes_without_ingredients(data: dict) -> list:
        """
        Process input dictionary and delete recipes without ingredients.
        This is needed as some scraped recipes are general articles or website code changed.
        This function in the future may be replaced by modifying scraper.py code.
        """
        found_recipes_list = []
        recipes_without_ingredients = {}

        for category, category_data in data.items():
            for recipe_name, recipe_data in category_data["recipes"].items():
                if recipe_data["content"].get("ingredients") is None:
                    found_recipes_list.append((category, recipe_name))
                    recipes_without_ingredients[category] = {'recipes': {recipe_name: recipe_data}}
                    save_data_to_json(recipes_without_ingredients, 'json_files/recipes_without_ingredients.json')
        print(f'Found {len(found_recipes_list)} recipes without ingredients.')
        return found_recipes_list

    for cat, recipe_to_delete in find_recipes_without_ingredients(recipes_input_data):
        del recipes_input_data[cat]["recipes"][recipe_to_delete]

    save_data_to_json(recipes_input_data, 'json_files/recipes_with_ingredients.json')


def check_new_recipes(data: dict) -> dict:
    recipes_from_first_page = {}
    for category, category_data in data.items():
        category_url = category_data['url']
        recipes_from_first_page[category] = scrape_recipes_urls(category, category_url, data,
                                                                check_only_first_page=True, )
    return recipes_from_first_page
