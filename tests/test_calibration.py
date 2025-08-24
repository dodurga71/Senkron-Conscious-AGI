from layer1_prediction_engine.calibration import (
    OnlineCalibration,
    brier_score,
    log_loss,
)


def test_brier_and_logloss_values():
    y = [1, 0, 1]
    p = [0.8, 0.3, 0.7]
    b = brier_score(y, p)  # (0.2^2 + 0.3^2 + 0.3^2)/3 = 0.073333...
    assert abs(b - 0.0733333333) < 1e-6
    ll = log_loss(y, p)
    assert 0.2 < ll < 0.7  # makul aralık (doğruluk testi)


def test_online_calibration_updates():
    oc = OnlineCalibration()
    oc.update_binary(1, 0.8)
    oc.update_binary(0, 0.3)
    oc.update_binary(1, 0.7)
    m = oc.metrics
    assert m["n"] == 3 and m["brier"] > 0 and m["logloss"] > 0
