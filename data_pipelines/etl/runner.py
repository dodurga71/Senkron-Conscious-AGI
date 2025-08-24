from __future__ import annotations
from typing import List, Dict, Any
from datetime import datetime, timezone
from pathlib import Path
import json

from data_curation.validator import validate_records
from data_pipelines.etl.transformers import pii_mask, reliability_tagging

def run_etl(raw_records: List[Dict[str, Any]], out_dir: str = "data-pipelines/output") -> Dict[str, Any]:
    """
    raw_records -> PII mask -> reliability -> doğrulama -> JSONL yaz
    Döndür: {"ok":int, "err":int, "outfile": Path}
    """
    curated = []
    for rec in raw_records:
        masked = pii_mask(rec, whitelist_keys={"headline"})
        rel = reliability_tagging(rec.get("source","social"), rec.get("meta", {}))
        curated.append({
            "timestamp": rec.get("timestamp", datetime.now(timezone.utc).isoformat()),
            "source": rec.get("source", "social"),
            "value": float(rec.get("value", 0.0)),
            "reliability_score": rel,
            "uncertainty_notes": rec.get("uncertainty_notes"),
            "cultural_diversity_flag": bool(rec.get("cultural_diversity_flag", False)),
        })

    v = validate_records(curated)
    ok = v["valid"]
    err = v["errors"]

    # yaz
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    outfile = out_path / f"curated_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.jsonl"
    with open(outfile, "w", encoding="utf-8") as f:
        for row in ok:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    return {"ok": len(ok), "err": len(err), "outfile": str(outfile)}
