FROM python:3.13-slim

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

RUN poetry install --no-dev && rm -rf $POETRY_CACHE_DIR

COPY . .

RUN cd src && python -m grpc_tools.protoc \
    --proto_path=../proto \
    --python_out=generated \
    --grpc_python_out=generated \
    ../proto/auth.proto

ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8000 50050

CMD ["poetry", "run", "python", "src/main.py"]
