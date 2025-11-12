FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    libjpeg-dev \
    zlib1g-dev \
    python3-dev \
    libpq-dev \
    curl \
    rustup \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set environment variables
ENV PATH="/root/.cargo/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT="/usr/local/"

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY pyproject.toml /app/
RUN uv sync --no-cache

# Copy application files
COPY . /app/

RUN chmod +x /app/start.sh

CMD ["sh", "/app/start.sh"]
