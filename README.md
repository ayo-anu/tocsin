# Tocsin

Tocsin is an incrementally developed backend for operational signal monitoring and incident response. The current increment provides a minimal HTTP application boundary and a non-production smoke route; monitoring features do not exist yet.

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

Start the local API on `127.0.0.1:8000`:

```bash
.venv/bin/tocsin-api
```

Verify the smoke route from another terminal:

```bash
curl --fail --silent http://127.0.0.1:8000/smoke
```

The deterministic response is:

```json
{"message":"Tocsin API is running."}
```

Run the focused checks:

```bash
.venv/bin/pytest
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/mypy src/tocsin
```
