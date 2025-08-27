from __future__ import annotations

from typing import Any


def _confidence_label(score: float) -> str:
    if score >= 0.75:
        return "yüksek"
    if score >= 0.45:
        return "orta"
    return "düşük"


def _format_drivers(source_details: list[dict[str, Any]], top_k: int = 3) -> str:
    if not source_details:
        return ""
    tops = source_details[:top_k]
    frags = []
    for d in tops:
        name = str(d.get("name", "")).replace("_predictor", "")
        c = float(d.get("contribution", 0.0))
        sign = "+" if c >= 0 else "-"
        frags.append(f"{name}({sign}{abs(c):.2f})")
    return ", ".join(frags)


def build_narrative(
    signal: float,
    uncertainty: float,
    reliability: float,
    sources: list[str] | None | None = None,
    source_details: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Bilge Rehber tarzı metin + şeffaflık alanları."""
    sources = sources or [
        "astro",
        "finance",
        "chaos",
        "quantum",
        "geopolitical",
        "social",
    ]

    conf_score = max(0.0, min(1.0, reliability * (1.0 - uncertainty)))
    conf_label = _confidence_label(conf_score)

    yön = "yukarı" if signal > 0 else ("aşağı" if signal < 0 else "nötr")
    kuvvet = abs(signal)
    kuvvet_etiket = "zayıf" if kuvvet < 0.08 else ("ılımlı" if kuvvet < 0.2 else "belirgin")

    drivers_txt = _format_drivers(source_details or [])
    driver_clause = f" Başlıca sürücüler: {drivers_txt}." if drivers_txt else ""

    narrative = (
        "Gözlemlediğimiz örüntüler, geçmiş yankılarla bugünün sinyallerini buluşturuyor. "
        f"Piyasa yönü {yön} ve {kuvvet_etiket} bir ivme gösteriyor. "
        f"Güven düzeyi {conf_label}; çünkü model güvenilirliği {reliability:.2f} ve "
        f"belirsizlik {uncertainty:.2f}. "
        "Bu bir kehanet değil; olasılık ufkunda bir rota önerisi. "
        "Adımlarını küçük riskle dene, çeşitlendir ve geri bildirim döngülerini kısa tut." + driver_clause
    )

    assumptions = [
        "Paralel modüllerin ( " + ", ".join(sources) + " ) ağırlıklı çıktıları kullanıldı.",
        "Kalibrasyon yer tutucu düzeydedir; üretimde Platt/Isotonic uygulanacaktır.",
        "Veri temel doğrulamadan geçti (tip/sınır kontrolleri).",
    ]
    risks = [
        "Veri kaynaklarında ani rejim değişimi (concept drift).",
        "Aşırı iyimser/karamsar sosyal gürültü.",
        "Likidite/düzenleyici haber akışı şokları.",
    ]

    source_summary = []
    for d in source_details or []:
        source_summary.append(
            {
                "name": d.get("name"),
                "reliability": round(float(d.get("reliability", 0.0)), 3),
                "uncertainty": round(float(d.get("uncertainty", 0.0)), 3),
                "contribution": round(float(d.get("contribution", 0.0)), 3),
            }
        )

    return {
        "narrative": narrative,
        "confidence": {"score": round(conf_score, 3), "label": conf_label},
        "assumptions": assumptions,
        "risks": risks,
        "source_summary": source_summary,
        "energy_cost": None,
    }
