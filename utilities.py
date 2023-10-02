from file_processing import load_data, save_data_to_json


def delete_recipes_without_ingredients(input_dict: dict):
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
        output_dict = {}

        for category, category_data in data.items():
            for recipe_name, recipe_data in category_data["recipes"].items():
                if recipe_data["content"].get("ingredients") is None:
                    found_recipes_list.append((category, recipe_name))
                    output_dict[category] = {'recipes': {recipe_name: recipe_data}}
                    save_data_to_json(output_dict, 'json_files/recipes_without_ingredients.json')
        print(f'Found {len(found_recipes_list)} recipes without ingredients.')
        return found_recipes_list

    for cat, recipe_to_delete in find_recipes_without_ingredients(input_dict):
        del input_dict[cat]["recipes"][recipe_to_delete]

    save_data_to_json(input_dict, 'json_files/recipes_with_ingredients.json')
