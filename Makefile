ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
DOCS_DIR := ${ROOT_DIR}/docs
DOCKER_FLAGS ?= --rm=true
DOCKER_BUILD_FLAGS ?= --force-rm=true --pull --rm=true
DOCKER_IMAGE := cybsi/cybsi-sdk
DOCKER_TAG ?= latest
VENV_DIR ?= .venv

lint:
	poetry run black cybsi examples
	poetry run flake8
	poetry run mypy cybsi
	poetry run isort cybsi tests examples

test:
	poetry run python3 -m unittest discover tests/ -v

build-docs:
	make -C ${DOCS_DIR} linkcheck html

.PHONY: image-build
image-build:
	docker build $(DOCKER_BUILD_FLAGS) --tag "$(DOCKER_IMAGE):$(DOCKER_TAG)" "$(ROOT_DIR)"

.PHONY: image-clean
image-clean: ### Remove last version of the images.
	docker rmi -f "$$(docker images -q $(DOCKER_IMAGE):$(DOCKER_TAG))"

docker-lint:
	docker run $(DOCKER_FLAGS) "$(DOCKER_IMAGE):$(DOCKER_TAG)" \
		make lint

docker-test:
	docker run $(DOCKER_FLAGS) "$(DOCKER_IMAGE):$(DOCKER_TAG)" \
		make test

docker-build-docs:
	mkdir -p docs/_build
	docker run -iv ${PWD}:/cybsi/ $(DOCKER_FLAGS) "$(DOCKER_IMAGE):$(DOCKER_TAG)" \
		sh -c "trap \"chown -R $$(id -u):$$(id -g) /cybsi/docs/_build\" EXIT; BUILDDIR=/cybsi/docs/_build make build-docs"

docker-clean:
	docker rmi -f "$$(docker images -q $(DOCKER_IMAGE):$(DOCKER_TAG))"

################ Helper targets ################
.PHONY: tools
tools: #### Install tools needed for development.
	pip3 install poetry==1.1.12
	poetry install