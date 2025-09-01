FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PYTHONPATH=/app/src

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

# Copy only requirements first for better cache usage
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry install --no-interaction --no-ansi --no-root

# Remove build-essential to reduce image size
RUN apt-get purge -y --auto-remove build-essential && rm -rf /var/lib/apt/lists/*

# Copy source code
COPY src ./src


EXPOSE 5000

CMD ["poetry", "run", "start"]