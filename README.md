# openapi-pytest-suite

Example output of an OpenAPI → pytest contract-suite generator, plus the landing page for the $99 service.

- `example/` is a real generated suite for the public Swagger Petstore OpenAPI 3 spec (`example/petstore-v3-openapi.json`).
- Run it with `pip install pytest && cd example && python3 -m pytest tests -q`. Dry run, no network: 19 passed, 9 skipped.
- The 9 skipped tests are the "request without credentials must be rejected" checks. They need a live API (`ATG_BASE_URL` and `ATG_DRY_RUN=0`), so they skip in dry run.
- The Petstore spec declares no server URL, so this example has not been run against any live API.

Landing page: https://arsenhambardzumyan.github.io/openapi-pytest-suite/

Built by Arsen Hambardzumyan, an independent developer in Yerevan.
