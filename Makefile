# Makefile to build, test, and run basic spec checks inside Docker

IMAGE_NAME := project-chimera:latest
CONTAINER_NAME := project-chimera-test

.PHONY: setup test spec-check

# Build the Docker image and install dependencies
setup:
	@echo "Building Docker image $(IMAGE_NAME)..."
	docker build -t $(IMAGE_NAME) .

# Run tests inside Docker (mounts current workspace)
test:
	@echo "Running tests inside Docker..."
	docker run --rm -v $(PWD):/workspace -w /workspace $(IMAGE_NAME) \
		/bin/sh -c "pip install --no-cache-dir -r requirements-dev.txt >/dev/null 2>&1 || true; pytest -q"

# Run an optional spec check inside Docker
spec-check:
	@echo "Running spec-check inside Docker..."
	docker run --rm -v $(PWD):/workspace -w /workspace $(IMAGE_NAME) \
		/bin/sh -c "sh scripts/spec_check.sh"
