.PHONY: install run web cli tui test lint clean

install:
	pip install -e ".[dev]"

run:
	python main.py

web:
	python main.py web

cli:
	python main.py --cli

tui:
	python main.py --tui

test:
	pytest

lint:
	ruff check .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache .ruff_cache data/ logs/