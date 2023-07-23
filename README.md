# Web Scraper with Beautiful Soup

This is my first project to portfolio, showing web scraper implemented using Beautiful Soup, 
a Python library for parsing HTML and XML documents.


## Description

This web scraper is design to extract recipes from the Bianca Zapatka blog.
It uses Beautiful Soup to navigate the HTML structure and retrieve desired elements based on specified selectors.

 

## Features

- Fetches recipes content from a [Bianca Zapatka blog](https://biancazapatka.com/)
- Parses the HTML using Beautiful Soup
- Extracts data based on specified CSS selectors
- Saves extracted data to JSON file for further processing

## Prerequisites

Make sure you have the following installed on your system:

- Python (version 3.x)
- Virtualenv (install using `pip install virtualenv`)

## Usage

1. Clone the repository:
   - Open Terminal.
   - Change the current working directory to the location where you want the cloned directory.
   - Type `git clone https://github.com/bartczak-pa/WebScraper.git`
   - Press Enter to create your local clone.

2. Create and activate a virtual environment:
   - Create virtual environment (type `python -m venv myenv`)
   - Activate virtual environment (type `source myenv/bin/activate'`)

3. Activate Script
   - Activate script by typing `python main.py`