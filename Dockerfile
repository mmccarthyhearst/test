FROM python:3.12-slim

WORKDIR /app

# Copy source before install so setuptools can find the package
COPY pyproject.toml .
COPY src/ src/

RUN pip install --no-cache-dir ".[ui]"

COPY alembic.ini .
COPY alembic/ alembic/
COPY scripts/ scripts/

EXPOSE 8000 8501

# Default: run the API (Railway overrides this via railway.toml startCommand)
CMD ["uvicorn", "ai_sdr.main:app", "--host", "0.0.0.0", "--port", "8000"]
