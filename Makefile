build:
	uv build

package-install:
	uv tool install --force dist/python_project_50-0.1.0-py3-none-any.whl

lint:
	uv tool run ruff check --fix gendiff
