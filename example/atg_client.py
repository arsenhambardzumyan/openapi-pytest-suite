"""atg_client - stdlib-only HTTP helper for the generated contract tests.

Secrets are never stored in this file. At runtime the client reads:
  ATG_BASE_URL      override the target base URL (spec default otherwise)
  ATG_API_TOKEN     sent as:  Authorization: Bearer <token>
  ATG_API_KEY       sent as:  X-API-Key: <key>
  ATG_DRY_RUN       default "1": no network, requests are simulated
"""
import json as _json
import os as _os
import urllib.parse as _up
import urllib.request as _ur


class Response:
    def __init__(self, status_code, text, url=""):
        self.status_code = status_code
        self.text = text
        self.url = url

    def json(self):
        return _json.loads(self.text)


class DryResponse(Response):
    """Simulated response carrying the documented expectation."""


_SAFE_METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS")


class Client:
    def __init__(self, base_url, dry_run=True):
        self.base_url = (base_url or "").rstrip("/")
        self.dry_run = dry_run

    def auth_headers(self):
        env = _os.environ
        if env.get("ATG_NO_AUTH"):
            return {}
        if env.get("ATG_API_TOKEN"):
            return {"Authorization": "Bearer " + env["ATG_API_TOKEN"]}
        if env.get("ATG_API_KEY"):
            return {"X-API-Key": env["ATG_API_KEY"]}
        return {}

    def request(
        self,
        method,
        path,
        query=None,
        body=None,
        headers=None,
        drop_credentials=False,
        expected_dry_status=200,
    ):
        method = str(method).upper()
        if method not in _SAFE_METHODS:
            raise ValueError("unsafe HTTP method: " + repr(method))
        if not self.base_url or not self.base_url.lower().startswith(("http://", "https://")):
            raise ValueError(
                "no usable base URL: set ATG_BASE_URL, or regenerate the suite "
                "from a spec that declares a server URL"
            )
        full = self.base_url + (path if str(path).startswith("/") else "/" + str(path))
        if query:
            full = full + ("&" if "?" in full else "?") + _up.urlencode(query)
        parsed = _up.urlsplit(full)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise ValueError("malformed request URL: " + full)

        ready = dict(headers or {})
        if not drop_credentials:
            ready.update(self.auth_headers())

        if self.dry_run:
            payload = _json.dumps(body) if body is not None else "{}"
            return DryResponse(int(expected_dry_status) or 200, payload, full)

        data = _json.dumps(body).encode("utf-8") if body is not None else None
        req = _ur.Request(full, data=data, headers=ready, method=method)
        with _ur.urlopen(req, timeout=30) as resp:  # noqa: S310
            text = resp.read(2_000_000).decode("utf-8", "replace")
            return Response(resp.status, text, full)
