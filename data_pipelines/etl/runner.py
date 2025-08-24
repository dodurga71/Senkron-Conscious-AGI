from __future__ import annotations

import json
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

from data_curation.validator import validate_records
from data_pipelines.etl.transformers import pii_mask, reliability_tagging


def _to_jsonable(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, date):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: _to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_to_jsonable(v) for v in obj]
    return obj


def run_etl(raw_records: list[dict[str, Any]], out_dir: str = "data-pipelines/output") -> dict[str, Any]:
    curated = []
    for rec in raw_records:
        rec = pii_mask(rec, whitelist_keys={"headline"})
        rel = reliability_tagging(rec.get("source", "social"), rec.get("meta", {}))
        curated.append(
            {
                "timestamp": rec.get("timestamp", datetime.now(UTC).isoformat()),
                "source": rec.get("source", "social"),
                "value": float(rec.get("value", 0.0)),
                "reliability_score": rel,
                "uncertainty_notes": rec.get("uncertainty_notes"),
                "cultural_diversity_flag": bool(rec.get("cultural_diversity_flag", False)),
            }
        )

    v = validate_records(curated)
    ok = v["valid"]
    err = v["errors"]

    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    outfile = out_path / f"curated_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.jsonl"
    with open(outfile, "w", encoding="utf-8") as f:
        for row in ok:
            row = _to_jsonable(row)
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    return {"ok": len(ok), "err": len(err), "outfile": str(outfile)}
