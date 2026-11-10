"""Bootstrap for the generated contract tests.

Dry run (no network) is ON by default so the suite is always collectable and
safe. To run against the real API:

    ATG_BASE_URL=https://api.example.com ATG_DRY_RUN=0 pytest tests/ -q
"""
import os as _os
import sys as _sys
from pathlib import Path as _Path

_SYS_ROOT = str(_Path(__file__).parent)
if _SYS_ROOT not in _sys.path:
    _sys.path.insert(0, _SYS_ROOT)

if _os.environ.get("ATG_DRY_RUN") is None:
    _os.environ["ATG_DRY_RUN"] = "1"
