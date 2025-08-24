from layer4_test_validation import compute_accuracy, measure_energy_usage


def test_metrics_and_energy():
    acc = compute_accuracy([1, 0, 1], [1, 1, 1])
    assert 0.0 <= acc <= 1.0
    energy = measure_energy_usage()
    assert "energy_proxy_seconds" in energy and energy["energy_proxy_seconds"] >= 0.0
