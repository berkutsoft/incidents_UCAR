FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    curl \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Установка uv
RUN pip install --no-cache-dir uv

ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock ./

# Create virtualenv and install deps from lockfile
RUN uv sync --frozen --no-dev --python /usr/local/bin/python

# Copy application code
COPY . .

EXPOSE 8600

ENV HOST=0.0.0.0 \
    PORT=8600

# Run the application using the uv-managed virtual environment
CMD ["uv", "run", "python", "wsgi.py"]


