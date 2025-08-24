"""
Katman 3 - Narrative Pipeline (İskelet)
- Transformers/LangChain eklenecek.
- Şimdilik: güvenli/denetlenebilir basit şablon üretimi.
"""

from typing import Any


def generate_narrative(context: dict[str, Any]) -> str:
    """
    Minimal anlatı üretimi (placeholder).
    """
    topic = context.get("topic", "genel")
    score = context.get("score", 0.0)
    return f"[SENKRON] Konu: {topic} | Skor: {score:.2f} | Not: İskelet anlatı"
