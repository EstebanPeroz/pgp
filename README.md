# My_pgp

A PGP-style encryption tool written in Python.

## Requirements

- Python 3.14+
- `make`

No other tooling is needed: the Makefile uses only the standard `venv` module and `pip`.

## Quick start

```sh
make          # create the virtualenv, install dependencies, build ./my_pgp
./my_pgp      # run the program
```

You can also run it as a module: `.venv/bin/python -m my_pgp`.

## Make targets

| Target       | Description                                                        |
|--------------|--------------------------------------------------------------------|
| `all`        | Default. Runs `init`, then symlinks the `./my_pgp` executable      |
| `init`       | Installs dependencies and the package          |
| `tests`      | Runs the test suite with `pytest`                                  |
| `clean`      | Removes caches and build artifacts                                 |
| `fclean`     | `clean`, plus removes `.venv` and `./my_pgp`                       |
| `re`         | `fclean`, then `all`                                               |

Use another interpreter with `make PYTHON=/path/to/python3.14`.

## Dependencies

`pyproject.toml` is the single source of truth. `requirements.txt` is a
generated lock file with exact versions. Do not edit it by hand.

To add a dependency:

1. Add it to `[dependency-groups]` in `pyproject.toml`.
2. Run `make`. `requirements.txt` is regenerated because `pyproject.toml` changed.
3. Commit both files.

## Project layout

```
.
├── pyproject.toml        # project metadata, dependencies, tool config
├── requirements.txt      # pinned dependencies (generated)
├── Makefile
├── src/
│   └── my_pgp/           # the package
│       ├── __init__.py
│       ├── __main__.py   # `python -m my_pgp`
│       └── main.py       # entry point: main()
├── tests/                # pytest test suite
└── docs/
```
