# My_pgp

A PGP-style encryption tool written in Python.

## Requirements

- Python 3.14+
- `make`

The program itself has no dependencies and runs with the system Python.
Development tools are installed in a local virtualenv with the standard
`venv` module and `pip`.

## Quick start

```sh
make          # build ./my_pgp (installs nothing)
./my_pgp      # run the program
```

You can also run it as a module: `PYTHONPATH=src python3 -m my_pgp`.

## Development

```sh
make dev                      # create .venv and install dev dependencies
make tests                    # run the test suite
.venv/bin/ruff check          # check the coding style
.venv/bin/ruff check --fix    # fix what can be fixed automatically
.venv/bin/ruff format         # format the code
```

The coding style (PEP 8, import order, common bugs, 79-character lines) is
configured in `pyproject.toml` under `[tool.ruff]`. The CI rejects any code
that does not pass `ruff check` and `ruff format --check`, or that contains
trailing whitespace.

## Make targets

| Target   | Description                                                      |
|----------|------------------------------------------------------------------|
| `all`    | Default. Symlinks `./my_pgp` to the program. Installs nothing    |
| `dev`    | Creates `.venv`, installs the locked dev dependencies and the    |
|          | pre-commit hook                                                  |
| `lock`   | Regenerates `requirements-dev.txt` from `pyproject.toml`         |
| `tests`  | Runs `dev`, then the test suite with `pytest`                    |
| `clean`  | Removes caches and build artifacts                               |
| `fclean` | `clean`, plus removes `.venv` and `./my_pgp`                     |
| `re`     | `fclean`, then `all`                                             |

Use another interpreter with `make PYTHON=/path/to/python3.14`.

## Dependencies

All dev dependency versions are pinned:

- `pyproject.toml` pins the direct dependencies (`dev` group of
  `[dependency-groups]`).
- `requirements-dev.txt` is the lock file: every package, including
  transitive ones, at an exact version. It is generated, do not edit it.
- `make dev` only installs from `requirements-dev.txt`. It never resolves
  new versions.

To add or upgrade a dev dependency:

1. Change its pinned version in the `dev` group of `pyproject.toml`.
2. Run `make lock`: it recreates `.venv` from scratch and regenerates
   `requirements-dev.txt`.
3. Run `make dev` and commit both files.

## Project layout

```
.
├── pyproject.toml        # project metadata, dependencies, tool config
├── requirements-dev.txt  # pinned dev dependencies (generated)
├── Makefile
├── .github/workflows/    # CI: style, build, run, tests
├── src/
│   └── my_pgp/           # the package
│       ├── __init__.py
│       ├── __main__.py   # `python -m my_pgp`
│       └── main.py       # entry point: main()
├── tests/                # pytest test suite
└── docs/
```
