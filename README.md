# Django REST Portfolio Backend Web Services

Welcome to the backend web services application for the Portfolio and Systems Architecture Platform. This application is powered by Python 3.12, Django 5.x, and Django REST Framework (DRF), exposing secure, structured JSON endpoints to fuel the frontend client.

---

## Core Technology Stack

- **Language**: Python 3.12 (optimized bytecode execution)
- **Framework**: Django 5.x with Django REST Framework (DRF)
- **Package Manager**: uv (high-speed Astral Python package manager)
- **Database**: PostgreSQL (Production) / SQLite3 (Development)
- **Static Assets**: WhiteNoise (zero-configuration static compression and serving)
- **Gateway Server**: Gunicorn 23.0.0 (pre-fork execution model)
- **Deployment**: Docker containerization on Render

---

## Directory Organization

The backend is architected using a modular application system. Core database models, custom managers, serializers, and views are isolated inside individual apps under `apps/`:

```text
backend/portfolio-backend/
├── apps/
│   ├── core/                  # Shared abstract models, managers, and exceptions
│   ├── users/                 # Custom user models and simple_jwt JWT token managers
│   ├── projects/              # Projects, Categories, and Technologies mappings
│   ├── blog/                  # Blog articles, Tags, and Likes systems
│   └── contact/               # Contact form submissions and email dispatches
│
├── config/                    # Core System Settings and Main Routing Dispatcher
│   ├── settings/              # Settings directory (base, local, production configs)
│   └── urls.py                # Primary URL router dispatcher
│
├── Dockerfile                 # Production Docker environment configuration
├── pyproject.toml             # uv package dependencies lists
└── uv.lock                    # Locked dependency tree mapping
```

For a comprehensive walkthrough of the backend app-based structure, database normalizations, and directory layouts, consult the detailed guide at:
👉 https://github.com/P-B37/docs/blob/main/backend_architecture.md

---

## Setup and Local Development Guide

### Step 1: Install uv Package Manager
We use Astral uv to manage Python packages. If missing on your machine:
```bash
# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex

# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 2: Initialize Virtual Environment
Navigate to this directory and synchronize dependencies:
```bash
# Automatically creates .venv and syncs uv.lock dependencies
uv sync
```

### Step 3: Run Database Migrations
Activate your virtual environment and generate database tables:
```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Apply schema migrations
python manage.py migrate

# (Optional) Seed superuser credentials for admin panel access
python manage.py createsuperuser
```

### Step 4: Run the Local Server
Launch the development server on port 8001:
```bash
python manage.py runserver 8001
```
The local API catalog will be serving at: http://127.0.0.1:8001/api/

---

## Core Systems & Database Implementations

Several advanced backend patterns have been engineered to ensure reliability, security, and extreme performance:

1. **Custom Soft Deletion Engine**: Overrides standard Django `.delete()` calls to flags rows as `is_deleted=True` using custom queryset managers, preventing database loss.
2. **Atomic Concurrency Clapping**: Uses Django SQL F-expressions (`F("claps_count") + amount`) to prevent concurrency race conditions during multi-user claps.
3. **Graceful Signal Delegation (exec)**: Docker CMD chains migrations and launches Gunicorn using `exec`, running Gunicorn as PID 1 to capture OS termination signals (`SIGTERM`) for zero-downtime rolling updates.
4. **LocMem Caching Overrides**: Dynamically switches cache backends to `LocMemCache` for extremely fast, sub-5ms loading times in production, while respecting `DISABLE_CACHE` and `CACHE_TIMEOUT` environment variables.

For full code implementations, detailed database mapping tables, and Gunicorn container process explanation, refer to the technical document:
👉 https://github.com/P-B37/docs/blob/main/backend_architecture.md

---

## DRF REST API Documentation Reference

To review the request/response payloads, query parameters, ordering parameters, and success status shapes of all Projects, Blog, and Contact endpoints, refer to the API Reference Manual:
👉 https://github.com/P-B37/docs/blob/main/api_reference.md
