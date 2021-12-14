ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
DOCKER_FLAGS ?= --rm=true
DOCKER_BUILD_FLAGS ?= --force-rm=true --pull --rm=true
DOCKER_IMAGE := cybsi/cybsi-sdk
DOCKER_TAG ?= latest
VENV_DIR ?= .venv

lint:
	black cybsi examples
	flake8
	mypy cybsi

test:
	python3 -m unittest discover tests/ -v


$(VENV_DIR): VIRTUALENV-exists
	virtualenv --python=python3 "$(VENV_DIR)"

.PHONY: venv
venv: $(VENV_DIR) venv-update

venv-update: $(VENV_DIR) requirements.txt docs/requirements.txt
	$(VENV_DIR)/bin/pip install -r requirements.txt
	$(VENV_DIR)/bin/pip install -r docs/requirements.txt

include docs/Makefile
build-docs: html dirhtml

.PHONY: image-clean
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
