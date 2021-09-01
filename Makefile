DOCKER_FLAGS := --rm=true $(DOCKER_NOROOT) --network=none
DOCKER_IMAGE := cybsi/cybsi-sdk
DOCKER_TAG ?= latest
DOCKER_NOROOT := -u $$(id -u):$$(id -g)

lint:
	flake8 --exclude=.venv --exclude=venv


docker-build:
	docker build --pull --rm --tag "$(DOCKER_IMAGE):$(DOCKER_TAG)" .

docker-lint:
	docker run $(DOCKER_FLAGS) "$(DOCKER_IMAGE):$(DOCKER_TAG)" \
	make lint

docker-clean:
	docker rmi -f "$$(docker images -q $(DOCKER_IMAGE):$(DOCKER_TAG))"
