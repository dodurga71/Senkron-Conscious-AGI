from __future__ import annotations

from typing import Any


def validate_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    ok = []
    errs = []
    for r in records:
        if "timestamp" not in r or "source" not in r or "value" not in r:
            errs.append({"record": r, "error": "missing_required_field"})
            continue
        ok.append(r)
    return {"valid": ok, "errors": errs}
