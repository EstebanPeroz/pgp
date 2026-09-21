PYTHON ?= python3
VENV   := .venv
PIP    := $(VENV)/bin/pip
MAIN   := src/my_pgp/main.py

NAME := my_pgp

all: $(NAME)

$(NAME): $(MAIN)
	ln -sfn $(MAIN) ./$(NAME)
	chmod +x $(NAME)

$(VENV):
	$(PYTHON) -m venv $(VENV)

requirements-dev.txt: pyproject.toml | $(VENV)
	$(PIP) install --group dev
	$(PIP) freeze > requirements-dev.txt

dev: requirements-dev.txt
	$(PIP) install -r requirements-dev.txt
	$(VENV)/bin/pre-commit install

tests: dev
	$(VENV)/bin/python -m pytest tests

clean:
	find . -path ./$(VENV) -prune -o -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .pytest_cache .ruff_cache *.egg-info build dist

fclean: clean
	rm -rf $(VENV)
	rm -rf $(NAME)

re: fclean all

.PHONY: all dev tests clean fclean re
