# Base image
FROM python:3.12-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV PATH="/app/.venv/bin:$PATH"

# set work directory
WORKDIR /app

# install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# INSTALL DEPENDENCIES
# copy only files needed for requirements first (for docker caching)
COPY pyproject.toml uv.lock /app/

# install dependencies
RUN uv sync --frozen --no-cache

# Copy the rest of the project code
COPY . /app/

# collect static files (whitenoise)
RUN python manage.py collectstatic --noinput

# expose the port
EXPOSE 8000

# COMMAND TO RUN THE APPLICATION
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
