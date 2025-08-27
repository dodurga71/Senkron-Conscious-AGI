from collections.abc import Iterable
from typing import Any

"""
Katman 2 - SENKRON-EFT API (Güncel)
- C_E durumu: varsa kovaryans benzeri matrisin Frobenius normu
- F_info = <K_R> - α * S_EE
Not: State içinde "cov" (liste/list of lists) yoksa güvenli fallback kullanılır.
"""


def _as_bounds(maybe_bounds: tuple[float, float] | None) -> tuple[float, float]:
    return maybe_bounds or (0.0, 0.0)


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
            return float(total**0.5)
    except Exception:
        return 0.0


def compute_CE(state: dict[str, Any]) -> float:
    """
    C_E durumu hesapla:
    - Eğer state["cov"] varsa Frobenius normu
    - Yoksa: len(state) tabanlı basit fallback
    """
    if not state:
        return 0.0
    cov = state.get("cov")
    if cov is not None:
        return float(_fro_norm(cov))
    return float(len(state))


def minimize_Finfo(expect_KR: float, alpha: float, S_EE: float) -> dict:
    """
    F_info = <K_R> - α * S_EE
    Dönüş: {'F_info': değer}
    """
    f_info = float(expect_KR) - float(alpha) * float(S_EE)
    return {"F_info": f_info}


def grid_minimize_finfo(expect_KR: float, S_EE: float, alphas) -> dict:
    """
    α ızgarasında F_info(α) = <K_R> - α·S_EE için argmin seç.
    Dönüş: {"alpha": α*, "F_info": f*}
    """
    alphas = list(alphas or [])
    if not alphas:
        return {"alpha": 0.0, "F_info": float(expect_KR)}
    best = None
    for a in alphas:
        f = float(expect_KR) - float(a) * float(S_EE)
        if best is None or f < best[1]:
            best = (float(a), f)
    if best is None:
        return {"alpha": 0.0, "F_info": float(expect_KR)}
    alpha_star, f_star = best
    return {"alpha": alpha_star, "F_info": f_star}
