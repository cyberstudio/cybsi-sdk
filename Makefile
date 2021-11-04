DOCKER_FLAGS := --rm=true $(DOCKER_NOROOT) --network=none
DOCKER_IMAGE := cybsi/cybsi-sdk
DOCKER_TAG ?= latest
DOCKER_NOROOT := -u $$(id -u):$$(id -g)

lint:
	flake8 && mypy cybsi_sdk

test:
	python3 -m unittest discover tests/ -v

build-docs:
	cd docs && make html

docker-build:
	docker build --pull --rm --tag "$(DOCKER_IMAGE):$(DOCKER_TAG)" .

docker-lint:
	docker run $(DOCKER_FLAGS) "$(DOCKER_IMAGE):$(DOCKER_TAG)" \
	sh -c "flake8 --exclude=.venv,venv && mypy cybsi_sdk"

docker-test:
	docker run $(DOCKER_FLAGS) "$(DOCKER_IMAGE):$(DOCKER_TAG)" \
	python3 -m unittest discover tests/ -v

# FIXME: Currently we mount latest code and docs to build container. Otherwise they can be outdated. Find a way to avoid it.
docker-build-docs:
	mkdir -p docs/_build && docker run -iv ${PWD}:/cybsi_sdk/ $(DOCKER_FLAGS) "$(DOCKER_IMAGE):$(DOCKER_TAG)" \
	sh -c "trap \"chown -R $$(id -u):$$(id -g) /cybsi_sdk/docs/_build && find /cybsi_sdk -type d -name '__pycache__' | xargs rm -rf\" EXIT; sphinx-build -b html -d /cybsi_sdk/docs/_build/doctrees /cybsi_sdk/docs /cybsi_sdk/docs/_build/html"

docker-clean:
	docker rmi -f "$$(docker images -q $(DOCKER_IMAGE):$(DOCKER_TAG))"
