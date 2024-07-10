FROM python:3.12-slim

RUN pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

COPY scraper ./scraper

COPY utilities ./utilities
COPY json_files ./json_files

copy main.py ./

RUN poetry install --without dev

ENTRYPOINT ["poetry", "run", "python", "/app/main.py"]


