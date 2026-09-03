.PHONY: help setup dev deploy clean

help:
	@echo "Content Repurposer - Development Commands"
	@echo ""
	@echo "  make setup       Install dependencies (backend + frontend)"
	@echo "  make dev         Run both backend & frontend locally"
	@echo "  make backend     Run backend only (Flask)"
	@echo "  make frontend    Run frontend only (Vite)"
	@echo "  make docker      Run everything in Docker"
	@echo "  make test        Run tests"
	@echo "  make clean       Remove build artifacts & node_modules"
	@echo ""

setup:
	@echo "Setting up Content Repurposer..."
	cp .env.example .env
	@echo "Backend..."
	cd backend && python -m venv .venv && \
	source .venv/bin/activate && \
	pip install -r requirements.txt
	@echo "Frontend..."
	cd frontend && npm install
	@echo "✓ Setup complete!"

dev:
	@echo "Starting Content Repurposer (backend + frontend)..."
	@echo ""
	@echo "Backend (http://localhost:5000)..."
	cd backend && source .venv/bin/activate && python app.py & \
	cd frontend && npm run dev
	@echo ""

backend:
	cd backend && source .venv/bin/activate && python app.py

frontend:
	cd frontend && npm run dev

docker:
	docker-compose up --build

docker-down:
	docker-compose down

test:
	@echo "Running tests..."
	cd backend && source .venv/bin/activate && pytest
	cd frontend && npm test

clean:
	rm -rf backend/.venv backend/__pycache__ backend/*.pyc
	rm -rf frontend/node_modules frontend/dist
	rm -rf .env

build-frontend:
	cd frontend && npm run build

deploy-frontend:
	cd frontend && npm run build && npm run preview

.DEFAULT_GOAL := help
