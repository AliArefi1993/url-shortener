# Dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry

# Configure Poetry not to use virtualenvs
RUN poetry config virtualenvs.create false

# Copy poetry files first for better caching
COPY pyproject.toml poetry.lock* ./

# Install dependencies only
RUN poetry install --no-root --without dev --no-interaction --no-ansi

# Copy project files
COPY . .

EXPOSE 8000

# Start app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
