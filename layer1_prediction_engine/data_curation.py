"""
Katman 1 - Veri Küratörlüğü ve Füzyon Arayüzü
- Etik/güvenilirlik kontrolleri (placeholder)
- Basit normalizasyon (placeholder)
- Çoklu veri füzyonu (placeholder)
Not: Minimal iskelet; ileride Dask/PyTorch eklenecek.
"""

from typing import Any


def curate_data(raw_events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Veri temizleme ve etik filtreleme (basit iskelet).
    - None alanları eler
    - Temel alanların varlığını doğrular (id, ts)
    """
    curated: list[dict[str, Any]] = []
    required = {"id", "ts"}
    for e in raw_events or []:
        if e is None:
            continue
        if not required.issubset(e.keys()):
            continue
        curated.append(e)
    return curated


def fuse_data(
    curated: list[dict[str, Any]],
    astro: dict[str, Any] | None = None,
    finance: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Çoklu kaynak füzyonu (minimal iskelet).
    Girdi: curated olay listesi + opsiyonel astro/finans sözlükleri
    Çıktı: 'fused'=True ve temel sayımlar.
    """
    return {
        "fused": True,
        "count": len(curated or []),
        "has_astro": bool(astro),
        "has_finance": bool(finance),
    }


def normalize_numeric_fields(rows, fields):
    """
    Basit min-max normalizasyonu [0,1].
    rows: List[Dict]; fields: List[str]
    Dönüş: (normalized_rows, stats) -> stats[field] = {"min": m, "max": M}
    Not: None/eksik değerler korunur.
    """
    if not rows:
        return rows, {f: {"min": None, "max": None} for f in fields}
    mins, maxs = {}, {}
    for f in fields:
        vals = [float(r.get(f)) for r in rows if r is not None and isinstance(r.get(f), int | float)]
        mins[f] = min(vals) if vals else None
        maxs[f] = max(vals) if vals else None

    out = []
    for r in rows:
        if r is None:
            continue
        rr = dict(r)
        for f in fields:
            v = rr.get(f)
            if isinstance(v, int | float) and mins[f] is not None and maxs[f] is not None and maxs[f] != mins[f]:
                rr[f] = (float(v) - mins[f]) / (maxs[f] - mins[f])
        out.append(rr)
    stats = {f: {"min": mins[f], "max": maxs[f]} for f in fields}
    return out, stats
