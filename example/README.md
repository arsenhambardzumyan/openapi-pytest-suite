# Swagger Petstore - OpenAPI 3.0 (v1.0.27) - generated contract tests

19 generated pytest contract test module(s), a stdlib-only client and this README.

## Contents
- `tests/`        - generated contract tests (happy path per documented operation)
- `atg_client.py` - stdlib-only HTTP client (dry-run aware)
- `conftest.py`   - test bootstrap (enables dry run by default)

## Security
No secrets are embedded anywhere in this zip. Give credentials at runtime:

```bash
export ATG_BASE_URL="https://your-api.example.com"   # optional override
export ATG_API_TOKEN="..."        # sent as Authorization: Bearer <token>
export ATG_API_KEY="..."          # sent as X-API-Key (if no Bearer token is set)
```

## Run
Python 3.9+ and `pip install pytest` (once). Then:

```bash
# dry run - no network, purely local validation of the request/response contract
python3 -m pytest tests/ -q

# live run against your API
ATG_DRY_RUN=0 ATG_API_TOKEN="..." python3 -m pytest tests/ -q
```

## What was validated at generation time
1. The spec parsed strictly (OpenAPI 3.x or Swagger 2.0 JSON/YAML).
2. Every generated module passed a Python syntax check (py_compile).
3. The whole suite ran green in dry-run mode with **no network access**.
4. The source spec declares NO server URL, so the tests were NOT run against any live API. Set ATG_BASE_URL (and ATG_DRY_RUN=0) on first live run.

## Honest limits
- Dry run proves the generated suite is internally consistent with the spec.
  It does not prove your API is reachable, behaves as documented, or that
  auth plumbing is configured for your environment.
- Per-operation coverage is documented behaviour only: the happy path and,
  for secured endpoints, a live-only check that requests without credentials
  are rejected (401/403). It cannot test undocumented app logic - add your own
  tests for that layer.
