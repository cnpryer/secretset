.PHONY: help clean lint fmt mt-check test pre-commit bench

help:
	@echo ""
	@echo "Use 'make <command>'"
	@echo ""
	@echo "commands"
	@echo "  .venv			    create venv and install dependencies"
	@echo "  clean				remove cleanable files"
	@echo "  lint				run linters"
	@echo "  fmt				run formaters"
	@echo "  fmt-check			run formatting check"
	@echo "  test				run all tests"
	@echo "  pre-commit			run pre-commit standardization"
	@echo ""
	@echo "Check the Makefile to know exactly what each target is doing."

.venv:
	@python -m venv .venv
	@cargo install --git https://github.com/mitsuhiko/rye rye
	@pre-commit install

clean:
	-@rm -rf .venv
	-@rm -fr `find . -name __pycache__`
	-@rm -rf .pytest_cache
	-@rm -rf .mypy_cache

lint-types:
	@rye run mypy \
		src \
		tests

lint: .venv lint-types
	@rye run ruff check .

fmt: .venv
	@rye run ruff check . --select "I" --fix
	@rye run black .

fmt-check: .venv
	@rye run ruff check . --select "I"
	@rye run black . --check

test: .venv
	@rye run pytest

pre-commit: test fmt-check lint
