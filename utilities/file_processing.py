import json
from pathlib import Path


# Function dumping scraped recipes to JSON file for further processing
def save_data_to_json(data: dict, filename: str) -> None:
    """Save data to json file."""
    with Path(filename).open("w") as file:
        json.dump(data, file)


# Helper function loading json file as recipes dictionary
def load_data(filename: Path) -> dict:
    """Load data from json file."""
    # TODO @Pawel: possibility of selecting file to load  # noqa: FIX002, TD003

    with Path.open(filename) as data:
        return json.load(data)
