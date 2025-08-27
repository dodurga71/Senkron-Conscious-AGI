from math import isclose, sqrt

from layer2_eft_core import compute_CE


def test_compute_ce_with_cov():
    cov = [[1.0, 0.0], [0.0, 1.0]]  # Frobenius = sqrt(2)
    ce = compute_CE({"cov": cov})
    assert isclose(ce, sqrt(2.0), rel_tol=1e-9)
