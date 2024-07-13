# Web Scraper with Beautiful Soup

This is my first project to portfolio, showing web scraper implemented using Beautiful Soup, 
a Python library for parsing HTML and XML documents.


## Description

This is my first portfolio project showing Python Codings skills.
This web scraper is designed to extract recipes from the [Bianca Zapatka Blog](https://biancazapatka.com/)

The app task is to scrape recipes from Culinary Blog and save them to JSON file. 

### Used libraries

**Beautiful Soup 4** - Well known web scraper which allows parse HTML files and extract desired data.

**tqdm** - Python library responsible for displaying progress bars

**FastAPI** - Modern, fast (high-performance), web framework for building APIs based on standard Python type hints.

## Features

- Fetches recipes content from a [Bianca Zapatka blog](https://biancazapatka.com/)
- Parses the HTML using Beautiful Soup
- Extracts data based on specified CSS selectors
- Saves extracted data to JSON file for further processing
- Serves the extracted data via FastAPI

## Prerequisites

Make sure you have the following installed on your system:

- Docker

## Usage

1. Clone the repository
2. Build Docker Image:
    - Run `docker build -t web-scraper .`
3. Run Docker Container:
    - Run `docker run -p 8000:8000 web-scraper`
