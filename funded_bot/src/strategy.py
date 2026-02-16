from src.models import MarketSnapshot, Signal


def generate_signal(snapshot: MarketSnapshot) -> Signal:
    long_bias = snapshot.ema_fast > snapshot.ema_slow
    short_bias = snapshot.ema_fast < snapshot.ema_slow

    bullish_confirmation = snapshot.close > snapshot.prev_close
    bearish_confirmation = snapshot.close < snapshot.prev_close

    if long_bias and bullish_confirmation:
        return Signal(side="BUY", reason="EMA trend up + bullish confirmation")

    if short_bias and bearish_confirmation:
        return Signal(side="SELL", reason="EMA trend down + bearish confirmation")

    return Signal(side="FLAT", reason="No valid setup")
