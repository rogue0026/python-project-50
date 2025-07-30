build:
	uv build

package-install:
	uv tool install --force dist/hexlet_code-0.1.0-py3-none-any.whl

lint:
	uv tool run ruff check --fix gendiff
