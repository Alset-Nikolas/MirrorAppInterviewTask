DUMP_IMAGE := alpine:3.15
PROJECT_CONFIG := mirror_back/pyproject.toml

.PHONY: dev.compose
dev.compose:
	@docker-compose up -d postgres rabbitmq redis portainer

.PHONY: dev.format
dev.format:
	@black --config mirror_back/pyproject.toml . && isort --settings-path mirror_back/pyproject.toml .

.PHONY: lint.bandit
lint.bandit:
	@bandit -c mirror_back/pyproject.toml -r .

.PHONY: lint.mypy
lint.mypy:
	@mypy --sqlite-cache --config-file=mirror_back/pyproject.toml

.PHONY: lint.flake8
lint.flake8:
	@flake8

.PHONY: lint.isort
lint.isort:
	@isort --check-only --diff --settings-path mirror_back/pyproject.toml .

.PHONY: lint.black
lint.black:
	@black --config mirror_back/pyproject.toml --check --diff .

.PHONY: lint
#lint: lint.bandit lint.flake8 lint.mypy lint.isort lint.black
lint: lint.bandit lint.isort lint.black

.PHONY: lint.black.fix
lint.black.fix:
	@black --config mirror_back/pyproject.toml .

.PHONY: lint.isort.fix
lint.isort.fix:
	@isort --settings-path mirror_back/pyproject.toml .

.PHONY: lint.fix
lint.fix: lint.black.fix lint.isort.fix

.PHONY: pre-commit
pre-commit:
	@pre-commit run --all-files
