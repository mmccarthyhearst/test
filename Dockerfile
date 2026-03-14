FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir -e ".[ui]"

COPY src/ src/
COPY alembic.ini .
COPY alembic/ alembic/

EXPOSE 8000 8501
