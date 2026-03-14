.PHONY: dev test lint migrate docker-up docker-down dashboard

# Development
dev:
	uvicorn ai_sdr.main:app --reload --port 8000

dashboard:
	streamlit run src/ai_sdr/ui/app.py

# Testing
test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=ai_sdr --cov-report=html

# Linting
lint:
	ruff check src/ tests/
	ruff format --check src/ tests/

fix:
	ruff check --fix src/ tests/
	ruff format src/ tests/

# Database
migrate:
	alembic upgrade head

migrate-new:
	alembic revision --autogenerate -m "$(msg)"

# Docker
docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f
