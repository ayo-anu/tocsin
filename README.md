# Tocsin

Tocsin is an incrementally developed backend for operational signal monitoring and incident response. Task 1.1 provides only the installable Python project skeleton; no HTTP API or monitoring features exist yet.

## Development setup

Python 3.12 is the currently tested development runtime. The package supports Python 3.12 and later.

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e ".[dev]"
```

Run the placeholder command:

```bash
.venv/bin/tocsin
```

Run the focused checks:

```bash
.venv/bin/pytest
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/mypy src/tocsin
```
