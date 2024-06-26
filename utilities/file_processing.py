"""Helper functions for file processing."""


import json
from pathlib import Path


def save_data_to_json(data: dict, filename: str) -> None:
    """Save data to json file."""
    with Path(filename).open("w") as file:
        json.dump(data, file)


def load_data(filename: Path) -> dict:
    """Load data from json file."""
    # TODO @Pawel: possibility of selecting file to load

    with Path.open(filename) as data:
        return json.load(data)
