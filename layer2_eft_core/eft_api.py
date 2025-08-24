"""
Katman 2 - SENKRON-EFT API (Güncel)
- C_E durumu: varsa kovaryans benzeri matrisin Frobenius normu
- F_info = <K_R> - α * S_EE
Not: State içinde "cov" (liste/list of lists) yoksa güvenli fallback kullanılır.
"""

from typing import Any, Dict, Iterable


def _fro_norm(matrix: Iterable[Iterable[float]]) -> float:
    try:
        # NumPy varsa kullan, yoksa saf Python hesapla
        try:
            import numpy as np  # type: ignore

            arr = np.asarray(matrix, dtype=float)
            return float(np.linalg.norm(arr, "fro"))
        except Exception:
            # Saf Python Frobenius
            total = 0.0
            for row in matrix:
                for v in row:
                    total += float(v) ** 2
            return total**0.5
    except Exception:
        return 0.0


def compute_CE(state: Dict[str, Any]) -> float:
    """
    C_E durumu hesapla:
    - Eğer state["cov"] varsa Frobenius normu
    - Yoksa: len(state) tabanlı basit fallback
    """
    if not state:
        return 0.0
    cov = state.get("cov")
    if cov is not None:
        return _fro_norm(cov)
    return float(len(state))


def minimize_Finfo(expect_KR: float, alpha: float, S_EE: float) -> dict:
    """
    F_info = <K_R> - α * S_EE
    Dönüş: {'F_info': değer}
    """
    f_info = float(expect_KR) - float(alpha) * float(S_EE)
    return {"F_info": f_info}
