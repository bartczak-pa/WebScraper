import json


# Function dumping scraped recipes to JSON file for further processing
def save_data_to_json(data: dict, filename: str):
    with open(filename, 'w') as file:
        json.dump(data, file)


# Helper function loading json file as recipes dictionary
def load_data(filename: str) -> dict:
    # TODO possibility of selecting file to load

    file = open(filename)
    data = json.load(file)
    return data
