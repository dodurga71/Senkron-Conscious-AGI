"""
Dask tabanlı veri boru hattı (iskelet).
- JSON array dosyasını okur (samples/raw_events_min.json gibi)
- Basit filtre/temizleme uygular
- Listeye döndürür
Not: Üretimde Dask DataFrame/Bag + kalıcı depolama önerilir.
"""

from __future__ import annotations

import json
from typing import Any

import dask.bag as db


def load_json_array(path: str) -> list[dict[str, Any]]:
    """Tek bir JSON-array dosyasını dask.bag ile işler (map/filter), liste döndürür."""
    # Dosyayı stdlib ile bir kerede oku, Dask ile paralel map/filter uygula:
    seq = json.loads(open(path, encoding="utf-8-sig").read())
    bag = db.from_sequence(seq, npartitions=max(2, len(seq) or 1))
    required = {"id", "ts"}
    bag = bag.filter(lambda e: isinstance(e, dict) and required.issubset(e.keys()))
    return list(bag.compute())
