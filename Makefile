format:
	ruff check . --fix --config=pyproject.toml
	black . --config=pyproject.toml

check:
	mypy . --config=pyproject.toml

.PHONY: check format