from __future__ import annotations
from typing import List, Dict, Any

def validate_records(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    ok = []
    errs = []
    for r in records:
        if "timestamp" not in r or "source" not in r or "value" not in r:
            errs.append({"record": r, "error": "missing_required_field"})
            continue
        ok.append(r)
    return {"valid": ok, "errors": errs}
