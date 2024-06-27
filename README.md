# Web Scraper with Beautiful Soup

This is my first project to portfolio, showing web scraper implemented using Beautiful Soup, 
a Python library for parsing HTML and XML documents.


## Description

This is my first portfolio project showing Python Codings skills.
This web scraper is designed to extract recipes from the [Bianca Zapatka Blog](https://biancazapatka.com/)

The app task is to scrape recipes from Culinary Blog and save them to JSON file. 

### Used libraries and 3rd party apps

**Beautiful Soup 4** - Well known web scraper which allows parse HTML files and extract desired data.

**tqdm** - Python library responsible for displaying progress bars

**Poetry** - For managing dependencies and build virtual environment

**Ruff** - Well known linter for Python

**Pytest** - For testing the app

**Docker** - For containerizing the app

## Features

- Fetches recipes content from a [Bianca Zapatka blog](https://biancazapatka.com/)
- Parses the HTML using Beautiful Soup
- Extracts data based on specified CSS selectors
- Saves extracted data to JSON file for further processing

## Prerequisites

Make sure you have the following installed on your system:

- Python (version 3.12)
- Docker

## Usage

1. Clone the repository:
   - Open Terminal.
   - Change the current working directory to the location where you want the cloned directory.
   - Type `git clone https://github.com/bartczak-pa/WebScraper.git`
   - Press Enter to create your local clone.

2. Create Docker Image
   - Open Terminal.
   - Change the current working directory to the location of the cloned repository.
   - Type `docker build -t webscraper .`

3. Activate Script
   - Activate script by typing `docker run -d webscraper`