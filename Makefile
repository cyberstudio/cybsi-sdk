DOCKER_FLAGS := --rm=true $(DOCKER_NOROOT) --network=none
DOCKER_IMAGE := cybsi/cybsi-sdk
DOCKER_TAG ?= latest
DOCKER_NOROOT := -u $$(id -u):$$(id -g)

lint:
	flake8 --exclude=.venv,venv && mypy cybsi_sdk

test:
	python3 -m unittest discover tests/ -v

docker-build:
	docker build --pull --rm --tag "$(DOCKER_IMAGE):$(DOCKER_TAG)" .

docker-lint:
	docker run $(DOCKER_FLAGS) "$(DOCKER_IMAGE):$(DOCKER_TAG)" \
	sh -c "flake8 --exclude=.venv,venv && mypy cybsi_sdk"

docker-test:
	docker run $(DOCKER_FLAGS) "$(DOCKER_IMAGE):$(DOCKER_TAG)" \
	python3 -m unittest discover tests/ -v

docker-clean:
	docker rmi -f "$$(docker images -q $(DOCKER_IMAGE):$(DOCKER_TAG))"
