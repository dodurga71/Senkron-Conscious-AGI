from __future__ import annotations

import json
from pathlib import Path
from typing import List, Tuple

TITLE = "Kalibrasyon Raporu"


def _read_jsonl(p: Path) -> List[dict]:
    if not p.exists():
        return []
    out = []
    for ln in p.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            out.append(json.loads(ln))
        except json.JSONDecodeError:
            continue
    return out


def generate_dashboard(metrics_dir: str, out_csv: str, out_md: str) -> Tuple[str, str]:
    mdir = Path(metrics_dir)
    rows = []
    for fp in sorted(mdir.glob("*.jsonl")):
        day = fp.stem  # YYYY-MM-DD
        recs = _read_jsonl(fp)
        if not recs:
            continue
        last = recs[-1]  # günün en güncel kaydı
        brier = float(last.get("brier", 0))
        logloss = float(last.get("logloss", 0))
        n = int(last.get("n", len(recs)))
        rows.append(
            {"date": day, "avg_brier": brier, "avg_logloss": logloss, "n_rows": n}
        )

    # CSV yaz
    csvp = Path(out_csv)
    csvp.parent.mkdir(parents=True, exist_ok=True)
    with csvp.open("w", encoding="utf-8", newline="") as f:
        f.write("date,avg_brier,avg_logloss,n_rows\n")
        for r in rows:
            f.write(f'{r["date"]},{r["avg_brier"]},{r["avg_logloss"]},{r["n_rows"]}\n')

    # MD yaz (başlık TR)
    mdp = Path(out_md)
    mdp.parent.mkdir(parents=True, exist_ok=True)
    total_days = len(rows)
    md = [f"# {TITLE}", "", f"Gün sayısı: {total_days}"]
    if rows:
        last_row = rows[-1]
        md += [
            "",
            f'**Son Gün ({last_row["date"]})**',
            f'- avg_brier: {last_row["avg_brier"]}',
            f'- avg_logloss: {last_row["avg_logloss"]}',
            f'- n_rows: {last_row["n_rows"]}',
        ]
    mdp.write_text("\n".join(md), encoding="utf-8")

    return str(csvp), str(mdp)
