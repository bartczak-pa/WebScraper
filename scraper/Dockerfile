# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Install Poetry version 1.8.3
RUN pip install poetry==1.8.3

# Set the working directory in the container
WORKDIR /app

# Copy only the pyproject.toml and poetry.lock to cache dependencies
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-root --no-dev

# Copy the scraper code into the container
COPY scraper/ scraper/
COPY utilities/ utilities/
COPY config/ config/
COPY logs/ logs/
COPY json_files/ json_files/
COPY main.py .


# Command to run the scraper
CMD ["poetry", "run", "python", "main.py"]
