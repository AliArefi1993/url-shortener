# URL Shortener

A simple URL shortener service built with Python. This project provides RESTful APIs to shorten URLs and redirect users to the original URLs.

## Features
- Shorten long URLs
- Redirect short URLs to original URLs
- MongoDB integration for persistent storage
- Dockerized FastAPI app (Python 3.13)
- Redis-backed rate limiting for multi-worker support
- Poetry for dependency management
- Dev tools: flake8, black, isort, mypy, pre-commit
- Unit and integration tests

## Project Structure
```
├── apis.py
├── docker-compose.yml
├── Dockerfile
├── main.py
├── models.py
├── pyproject.toml
├── schemas.py
├── test_main.py
├── rate_limit.py
│   ├── rate_limit.py
├── app/
│   ├── apis.py
│   ├── models.py
│   ├── repository.py
│   ├── schemas.py
│   └── __pycache__/
├── tests/
│   ├── conftest.py
│   ├── test_url.py
│   └── __pycache__/
```

## Getting Started

### Prerequisites
- Python 3.13+
- Docker & Docker Compose

### Installation
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd url-shortener
   ```
2. Install dependencies with Poetry:
   ```bash
   poetry install
   ```

### Running with Docker
1. Build and start services:
   ```bash
   docker compose up --build
   ```
2. The API will be available at `http://localhost:8000`
3. MongoDB will be available at `mongodb://localhost:27017/url_shortener`
4. Redis will be available at `redis://localhost:6379/0` for rate limiting

### Running Locally
1. Start MongoDB and Redis locally or via Docker.
2. Run the app:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## API Endpoints
- `POST /shorten` - Shorten a URL (rate limited: 5 requests/minute per IP)
- `GET /{short_url}` - Redirect to original URL (rate limited: 20 requests/minute per IP)
- `GET /health` - Health check endpoint
- `GET /doc` - Interactive API documentation (Swagger UI)

## Testing
Run all tests:
```bash
MONGO_DB=url_shortener_test poetry run pytest tests
```

## Environment Variables
- `MONGO_URI`: MongoDB connection string
- `MONGO_DB`: MongoDB database name
- `REDIS_URL`: Redis connection string (default: `redis://localhost:6379/0`)

## Development
Dev dependencies are managed with Poetry and grouped under `[tool.poetry.dev-dependencies]` in `pyproject.toml`.
Recommended tools: flake8, black, isort, mypy, pre-commit.

## License
MIT
