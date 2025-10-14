# Makefile for Python environment setup with uv, named venv, pre-commit, Black, Ruff

.PHONY: all env precommit clean setup test

# Name of the virtual environment
VENV_NAME:=.venv

# Default target: setup environment and pre-commit
all: env precommit

# Create virtual environment and install dependencies
env:
	@if [ ! -d "$(VENV_NAME)" ]; then \
		echo "=========================================================="; \
		echo "Creating virtual environment named $(VENV_NAME)..."; \
		echo "=========================================================="; \
		uv venv --name $(VENV_NAME) --python 3.10; \
		uv pin python==3.10; \
		echo "=========================================================="; \
		echo "Upgrading pip, setuptools, wheel..."; \
		echo "=========================================================="; \
		uv add pip setuptools wheel --upgrade; \
		echo "=========================================================="; \
		echo "Adding project dependencies from requirements.txt..."; \
		echo "=========================================================="; \
		uv add -r grpc_ext/requirements.txt; \
		echo "=========================================================="; \
		echo "Adding dev tools: pre-commit, black, ruff..."; \
		echo "=========================================================="; \
		uv add requirements-dev.txt; \
	else \
		echo "Virtual environment $(VENV_NAME) already exists — skipping creation."; \
	fi


# Setup pre-commit hooks
precommit:
	@echo "Installing pre-commit hooks..."
	. $(VENV_NAME)/bin/activate && pre-commit install
	@echo "Pre-commit hooks installed successfully."

# Launch the setup
setup: env precommit
	@echo "=========================================================="
	@echo "Turning down server if any and removing orphans"
	@echo "=========================================================="
	cd docker/ && docker compose down --volumes --remove-orphans
	@echo "=========================================================="
	@echo "Building no-cache images"
	@echo "=========================================================="
	cd docker/ && docker compose -f docker-compose-grpc.yml build --no-cache

# Launch the ragflow and grpc servers
up:
	@echo "=========================================================="
	@echo "Launching servers"
	@echo "=========================================================="
	cd docker/ && docker compose -f docker-compose-grpc.yml up -d
	@echo "=========================================================="
	@echo "Running tests against live servers"
	@echo "=========================================================="
	$(MAKE) test

# Turning down the servers and removing orphans
down:
	@echo "Turning down the servers if any and removing orphans"
	cd docker/ && docker compose down --volumes --remove-orphans

# Tests for testing ragflow's endpoints and grpc client-server communication to ragflow
test:
	@echo "=========================================================="
	@echo "Testing launched servers along with grpc client"
	@echo "=========================================================="
	cd grpc_ext/grpc_server/ && uv run pytest -v endpoint_test.py grpc_async_ragclient_test.py

# Build sphinx like documentation for codes within grpc_ext/
docs:
	@echo "=========================================================="
	@echo "Building documentation..."
	@echo "=========================================================="
	cd grpc_ext/ && make -C docs html
