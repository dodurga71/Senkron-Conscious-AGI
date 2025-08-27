from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None  # type: ignore


def load_config(path: str | None = None) -> dict[str, Any]:
    p = Path(path or "config/default.yaml")
    if yaml and p.exists():  # type: ignore[truthy-bool]
        return yaml.safe_load(p.read_text(encoding="utf-8")) or {}  # type: ignore[attr-defined]
    return {}
