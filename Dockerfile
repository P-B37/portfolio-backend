# Base image
FROM python:3.12-slim

# set environment variable
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# poetry specific settings to disable virtualenvs cause the container is the env
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_CACHE_DIR='/var/cache/pypoetry'
ENV POETRY_HOME='/usr/local'

# set work directory
WORKDIR /app

# install syatem dependancies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# install Poetry
RUN pip install --no-cache-dir  poetry

# INSTALL DEPENDENCIES
# copy only files neede for requirements first (for docker caching)
COPY pyproject.toml poetry.lock /app/

# install dependencies (exculding the project itself)
RUN poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the project code
COPY . /app/

# collect static files (whitenoise)
RUN poetry run python manage.py collectstatic --noinput

# expose the port
EXPOSE 8000

# COMMAND TO RUN THE APPLICATION
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
