from dataclasses import dataclass


@dataclass
class BacktestMetrics:
    trades: int
    wins: int
    losses: int
    profit_factor: float
    max_drawdown_pct: float
    violations: int


def evaluate_stub() -> BacktestMetrics:
    """
    Placeholder metrics for pipeline wiring.
    Real implementation should use historical candles/ticks and strategy loop.
    """
    return BacktestMetrics(
        trades=120,
        wins=68,
        losses=52,
        profit_factor=1.31,
        max_drawdown_pct=4.8,
        violations=0,
    )
