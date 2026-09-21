PYTHON ?= python3
VENV   := .venv
PIP    := $(VENV)/bin/pip
MAIN   := src/my_pgp/main.py

NAME := my_pgp

all: init $(NAME)

$(VENV):
	$(PYTHON) -m venv $(VENV)

$(NAME): $(MAIN)
	ln -sn $(MAIN) ./$(NAME)
	chmod +x $(NAME)

requirements.txt: pyproject.toml | $(VENV)
	$(PIP) install --group dev
	$(PIP) freeze > requirements.txt

init: requirements.txt
	$(PIP) install -r requirements.txt

tests: init
	$(VENV)/bin/python -m pytest tests

clean:
	find . -path ./$(VENV) -prune -o -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .pytest_cache *.egg-info build dist

fclean: clean
	rm -rf $(VENV)
	rm -rf $(NAME)

re: fclean all

.PHONY: all init tests clean fclean re
