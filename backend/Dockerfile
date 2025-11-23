# Backend service image built with uv
FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/app/.venv

WORKDIR /app

# System deps for psycopg2 and building wheels
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install uv (fast Python package manager)
RUN pip install --no-cache-dir uv

# Install dependencies first to leverage Docker cache
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy the rest of the application
COPY . .

ENV PATH="/app/.venv/bin:${PATH}"

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
