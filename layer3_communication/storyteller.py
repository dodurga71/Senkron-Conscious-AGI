from __future__ import annotations
from typing import Dict, Any, List

def _confidence_label(score: float) -> str:
    # score ~ [0..1] -> etiket
    if score >= 0.75:
        return "yüksek"
    if score >= 0.45:
        return "orta"
    return "düşük"

def build_narrative(signal: float, uncertainty: float, reliability: float, sources: List[str] | None = None) -> Dict[str, Any]:
    """
    Bilge Rehber tarzında metin üretir ve şeffaflık alanlarını döndürür.
    """
    sources = sources or ["astro", "finance", "chaos", "quantum", "geopolitical", "social"]
    # 0..1 arası genel güven puanı: güvenilirlik * (1 - belirsizlik)
    conf_score = max(0.0, min(1.0, reliability * (1.0 - uncertainty)))
    conf_label = _confidence_label(conf_score)

    yön = "yukarı" if signal > 0 else ("aşağı" if signal < 0 else "nötr")
    kuvvet = abs(signal)
    kuvvet_etiket = "zayıf" if kuvvet < 0.08 else ("ılımlı" if kuvvet < 0.2 else "belirgin")

    narrative = (
        "Gözlemlediğimiz örüntüler, geçmiş yankılarla bugünün sinyallerini buluşturuyor. "
        f"Piyasa yönü {yön} ve {kuvvet_etiket} bir ivme gösteriyor. "
        f"Güven düzeyi {conf_label}; çünkü model güvenilirliği {reliability:.2f} ve belirsizlik {uncertainty:.2f}. "
        "Bu bir kehanet değil; olasılık ufkunda bir rota önerisi. "
        "Adımlarını küçük riskle dene, çeşitlendir ve geri bildirim döngülerini kısa tut."
    )

    assumptions = [
        "Paralel modüllerin ( " + ", ".join(sources) + " ) ağırlıklı çıktıları kullanıldı.",
        "Kalibrasyon yer tutucu düzeydedir; üretimde Platt/Isotonic uygulanacaktır.",
        "Veri temel doğrulamadan geçti (tip/sınır kontrolleri)."
    ]
    risks = [
        "Veri kaynaklarında ani rejim değişimi (concept drift).",
        "Aşırı iyimser/karamsar sosyal gürültü.",
        "Likidite/düzenleyici haber akışı şokları."
    ]

    return {
        "narrative": narrative,
        "confidence": {"score": round(conf_score, 3), "label": conf_label},
        "assumptions": assumptions,
        "risks": risks,
        "energy_cost": None  # ileride CodeCarbon ölçümü eklenebilir
    }
