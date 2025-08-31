FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PYTHONPATH=/app/src

RUN apt-get update && \
    apt-get install -y curl build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* ./
COPY src ./src

RUN poetry install --no-interaction --no-ansi

EXPOSE 5000

CMD ["poetry", "run", "start"]