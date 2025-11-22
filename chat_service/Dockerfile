FROM python:latest

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

COPY . .

ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

EXPOSE 50051

CMD ["poetry", "run", "python", "src/main.py"]