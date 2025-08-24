from __future__ import annotations
from pathlib import Path
from typing import List, Tuple, Dict, Any
import json, csv

def _read_jsonl(p: Path) -> List[dict]:
    if not p.exists():
        return []
    out: List[dict] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except Exception:
            # bozuk satırı atla
            pass
    return out

def _aggregate(rows: List[dict]) -> Dict[str, Any]:
    briers = [r.get("brier") for r in rows if isinstance(r.get("brier"), (int, float))]
    logs   = [r.get("logloss") for r in rows if isinstance(r.get("logloss"), (int, float))]
    return {
        "avg_brier": (sum(briers) / len(briers)) if briers else None,
        "avg_logloss": (sum(logs) / len(logs))   if logs   else None,
        "n_rows": len(rows),
    }

def generate_dashboard(metrics_dir: str, out_csv: str, out_md: str) -> Tuple[str, str]:
    """
    metrics_dir altındaki *.jsonl dosyalarını okuyup
    günlük özetleri CSV ve Markdown olarak üretir.
    Dönüş: (csv_path, md_path)
    """
    mdir = Path(metrics_dir)
    mdir.mkdir(parents=True, exist_ok=True)
    files = sorted(mdir.glob("*.jsonl"))

    history: List[Tuple[str, Any, Any, int]] = []
    for f in files:
        day = f.stem  # YYYY-MM-DD
        agg = _aggregate(_read_jsonl(f))
        history.append((day, agg["avg_brier"], agg["avg_logloss"], agg["n_rows"]))

    # CSV
    csv_path = Path(out_csv)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as w:
        writer = csv.writer(w)
        writer.writerow(["date", "avg_brier", "avg_logloss", "n_rows"])
        for day, b, l, n in history:
            writer.writerow([day,
                             (None if b is None else round(b, 6)),
                             (None if l is None else round(l, 6)),
                             n])

    # Markdown
    md_path = Path(out_md)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Kalibrasyon Raporu", "", f"Gün sayısı: {len(history)}"]
    if history:
        day, b, l, n = history[-1]
        lines += [
            "",
            f"**Son Gün ({day})**",
            f"- avg_brier: {None if b is None else round(b, 6)}",
            f"- avg_logloss: {None if l is None else round(l, 6)}",
            f"- n_rows: {n}",
        ]
    md_path.write_text("\n".join(lines), encoding="utf-8")

    return (str(csv_path), str(md_path))


