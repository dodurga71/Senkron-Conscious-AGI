from __future__ import annotations
from typing import Dict, Any
import re

_EMAIL_RE = re.compile(r"([A-Za-z0-9._%+-]+)@([A-Za-z0-9.-]+\.[A-Za-z]{2,})")
_PHONE_RE = re.compile(r"\b(\+?\d[\d\-\s]{7,}\d)\b")

SENSITIVE_KEYS = {
    "email", "e_mail", "mail",
    "phone", "tel", "gsm",
    "tc_kimlik", "ssn", "national_id",
    "name", "fullname"
}

def mask_email(s: str) -> str:
    def _m(m):
        user, dom = m.group(1), m.group(2)
        if len(user) <= 2:
            masked = "*" * len(user)
        else:
            masked = user[0] + "*"*(len(user)-2) + user[-1]
        return masked + "@" + dom
    return _EMAIL_RE.sub(_m, s)

def mask_phone(s: str) -> str:
    return _PHONE_RE.sub(lambda m: m.group(1)[:2] + "*"*(len(m.group(1))-4) + m.group(1)[-2:], s)

def mask_value(k: str, v: Any):
    if not isinstance(v, str):
        return v
    out = v
    out = mask_email(out)
    out = mask_phone(out)
    return out

def pii_mask(record: Dict[str, Any], whitelist_keys: set[str] | None = None) -> Dict[str, Any]:
    wl = whitelist_keys or set()
    out = {}
    for k, v in record.items():
        kl = k.lower()
        if kl in wl:
            out[k] = v
        elif kl in SENSITIVE_KEYS:
            if isinstance(v, str): out[k] = "***"
            else: out[k] = None
        else:
            out[k] = mask_value(k, v)
    return out

def reliability_tagging(source: str, meta: Dict[str, Any]) -> float:
    """
    Çok basit sezgisel puanlayıcı:
    - Kaynak türüne göre taban puan
    - citation_count ve verified_source ile artı/eksi
    """
    base = {
        "finance": 0.75,
        "astro": 0.55,
        "history": 0.7,
        "social": 0.5
    }.get(source, 0.5)
    cit = float(meta.get("citation_count", 0.0))
    ver = 1.0 if meta.get("verified_source") else 0.0
    score = base + min(0.15, cit * 0.01) + ver * 0.1
    return max(0.0, min(1.0, score))
