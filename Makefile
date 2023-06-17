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
	$(SOURCE_VENV) && cd src/rest  && uvicorn api:app --reload

pre-commit: venv
	$(SOURCE_VENV) && pre-commit clean && pre-commit install && pre-commit run

docker-build:
	docker rmi -f app || true
	docker build -t app .

up:
	docker compose up -d

linux:
	docker exec -it linux-machine-for-testing zsh

psql:
	docker exec -it linux-machine-for-testing psql -h db -U metabase -d metabase

serialised_rmq: docker-build
	PYTHONPATH="${PYTHONPATH}:/app" python3 ./architectures/serialised_rmq.py

orchestrator: docker-build
	PYTHONPATH="${PYTHONPATH}:/app" python3 ./architectures/orchestrator.py

serialised_orchestrator: docker-build
	PYTHONPATH="${PYTHONPATH}:/app" python3 ./architectures/serialised_orchestrator.py

async_orchestrator: docker-build
	PYTHONPATH="${PYTHONPATH}:/app" python3 ./architectures/async_orchestrator.py


clean_before_rerun:
	docker exec -it linux-machine-for-testing psql -h db -U metabase -d metabase -c "truncate total_load;"
	docker exec -it linux-machine-for-testing psql -h db -U metabase -d metabase -c "truncate daily_total_load;"
	docker exec -it linux-machine-for-testing psql -h db -U metabase -d metabase -c "truncate weekly_total_load;"
	docker exec -it linux-machine-for-testing psql -h db -U metabase -d metabase -c "truncate monthly_total_load;"
	-docker exec -it linux-machine-for-testing root/rpk/rpk topic delete test_topic --brokers 'redpanda-0:9092'
	-docker exec -it rabbitmq rabbitmqctl delete_queue daily
	-docker exec -it rabbitmq rabbitmqctl delete_queue monthly
	-docker exec -it rabbitmq rabbitmqctl delete_queue weekly

soa_redpanda: docker-build
	PYTHONPATH="${PYTHONPATH}:/app" python3 ./architectures/soa_redpanda.py

kill-workers:
	docker ps --filter name=-worker -aq | xargs -r docker stop | xargs -r docker rm

down: kill-workers
	docker compose down
	docker volume prune --force --all
