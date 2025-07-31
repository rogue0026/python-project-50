install:
	@uv sync

build:
	@uv build

package-install:
	@uv tool install --force dist/hexlet_code-0.1.0-py3-none-any.whl

lint:
	@uv run ruff check diffcalculator

test:
	@uv run pytest

test-coverage:
	@uv run pytest --cov=diffcalculator --cov-report xml

check: lint test