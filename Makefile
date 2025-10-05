.PHONY: help install install-dev test test-cov test-real clean build dist lint format check example server-deps test-server

help: ## Mostra aquesta ajuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instal·la el paquet en mode desenvolupament
	pip install -e .

install-dev: ## Instal·la dependències de desenvolupament
	pip install -r requirements-dev.txt
	pip install -e .

server-deps: ## Instal·la dependències del servidor progressiu
	pip install flask flask-cors requests

test: ## Executa els tests
	python -m pytest tests/

test-cov: ## Executa els tests amb cobertura
	python -m pytest tests/ --cov=whatsapp_chat_reader --cov-report=html --cov-report=term

test-real: server-deps ## Executa tests amb l'exemple real
	python -m pytest tests/test_real_example.py -v

test-server: server-deps ## Inicia servidor amb l'exemple real
	python3 progressive_server.py "tests/real-example-test/_chat.txt" --attachments "tests/real-example-test" --chat-name "Real Example Test Chat" --port 8080

lint: ## Executa el linter
	flake8 src/ tests/
	mypy src/

format: ## Formata el codi
	black src/ tests/

check: lint test ## Executa linting i tests

clean: ## Neteja fitxers temporals
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean ## Construeix el paquet
	python -m build

dist: build ## Crea distribució
	twine check dist/*

example: ## Executa l'exemple
	python whatsapp_chat_reader.py examples/exemple_chat.txt --attachments-dir examples --output examples/exemple_output.html --open
