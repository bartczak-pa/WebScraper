import json


# Function dumping scraped recipes to JSON file for further processing
def save_recipes_to_json(recipes_dict: dict):
    filename = 'recipes.json'

    with open(filename, 'w') as file:
        json.dump(recipes_dict, file)
        print(f'Recipes has been saved to {filename} file.')


# Helper function loading json file as recipes dictionary
def load_recipes() -> dict:
    # TODO possibility of selecting file to load

    file = open('recipes.json')
    data = json.load(file)
    return data
