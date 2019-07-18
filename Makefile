PIPENV=.venv
PYTHON_VERSION=3.6.5

.PHONY: all dev

all: install

$(PIPENV):
	env PIPENV_VENV_IN_PROJECT=$(PIPENV) pipenv --python $(PYTHON_VERSION)
	pipenv run python -m pip install -U pip==19.1.1

install: $(PIPENV)
	pipenv install

dev: install
	pip install pre-commit
	pre-commit install-hooks
	pipenv install -d

docker:
	docker-compose up -d

requirements:
	pipenv run pipenv_to_requirements
