import math


def _sharpe(returns, eps=1e-12):
    # basit günlük Sharpe: mean/std * sqrt(252)
    if len(returns) < 2:
        return 0.0
    mu = sum(returns) / len(returns)
    var = sum((r - mu) ** 2 for r in returns) / (len(returns) - 1)
    sd = math.sqrt(max(var, eps))
    return (mu / (sd + eps)) * math.sqrt(252)


def backtest_with_pandas(prices, signal_series, fee_bps=5):
    """
    prices: list[float]
    signal_series: list[float] (-1..+1)
    """
    returns = []
    pos_prev = 0.0
    for i in range(1, len(prices)):
        pos = max(-1.0, min(1.0, signal_series[i]))
        ret = pos * ((prices[i] - prices[i - 1]) / prices[i - 1])
        # basit işlem maliyeti
        if pos != pos_prev:
            ret -= fee_bps / 10000.0
        returns.append(ret)
        pos_prev = pos
    return {"sharpe": _sharpe(returns), "cumret": float(sum(returns))}


def run_backtest(prices, signal_series, use_backtrader: bool = False) -> dict[str, float]:
    # CodeCarbon opsiyonel
    tracker = None
    try:
        from codecarbon import EmissionsTracker

        tracker = EmissionsTracker(log_level="error", measure_power_secs=1, offline=True)
        tracker.start()
    except Exception:
        tracker = None

    try:
        if use_backtrader:
            # Hafif tutmak için pandas sürümünü kullanıyoruz (CI hızlı kalsın)
            return backtest_with_pandas(prices, signal_series)
        else:
            return backtest_with_pandas(prices, signal_series)
    finally:
        if tracker:
            try:
                tracker.stop()
            except Exception:
                pass
