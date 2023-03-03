SHELL := /bin/bash
SOURCE_VENV := source venv/bin/activate

PYTHON_INTERPRETER := python3.10
PIP := $(PYTHON_INTERPRETER) -m pip
VENV_DIR = venv

DOCKER_SERVER_IMAGE_TAG := api-stress-testing
DOCKER_IMAGE_VERSION := latest
DOCKER_EXPOSE_PORT := 8081
PIP := python -m pip

.PHONY: clean venv lint docker_build docker_clean redis_up tests serve

# Removes the existing virtual environment, if exists
clean:
	-deactivate
	rm -rf venv

# Create a Python virtual environment
venv:
	$(PYTHON_INTERPRETER) -m venv $(VENV_DIR)
	$(SOURCE_VENV) && $(PIP) install --upgrade pip
	$(SOURCE_VENV) && $(PIP) install -r requirements.txt

# Lint-check the code in the virtual environment
lint: venv
	$(SOURCE_VENV) && scripts/lint.sh

test: venv
	$(SOURCE_VENV) && pytest

run: venv
	$(SOURCE_VENV) && $(PYTHON_INTERPRETER) run.py

run-api: venv
	$(SOURCE_VENV) && cd src/api  && uvicorn api:app --reload

pre-commit: venv
	$(SOURCE_VENV) && pre-commit clean && pre-commit install && pre-commit run

docker-build:
	docker build -t app .

up: docker-build
	docker compose up -d

down:
	docker compose down
