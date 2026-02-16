import unittest
from datetime import datetime

from src.models import AccountState, MarketSnapshot, Signal
from src.risk_engine import RiskEngine, RuleViolation


class RiskEngineTests(unittest.TestCase):
    def base_config(self):
        return {
            "account": {
                "starting_balance": 100000,
                "max_daily_drawdown_pct": 5.0,
                "max_overall_drawdown_pct": 10.0,
                "max_lot_size": 2.0,
                "max_open_positions": 1,
                "max_total_exposure_lots": 2.0,
            },
            "trading": {
                "risk_per_trade_pct": 0.5,
                "rr_ratio": 1.5,
                "max_spread_points": 25,
                "max_slippage_points": 15,
            },
            "sessions": {"allowed_windows": [{"start": "00:00", "end": "23:59"}]},
            "news_filter": {
                "enabled": True,
                "block_before_minutes": 30,
                "block_after_minutes": 30,
            },
        }

    def base_account(self):
        return AccountState(
            balance=100000,
            equity=100000,
            day_start_balance=100000,
            open_positions=0,
            open_lots=0.0,
        )

    def base_snapshot(self, now):
        return MarketSnapshot(
            symbol="EURUSD",
            time=now,
            bid=1.1,
            ask=1.1002,
            spread_points=10,
            slippage_points=5,
            ema_fast=1.2,
            ema_slow=1.1,
            atr=0.001,
            close=1.2,
            prev_close=1.19,
        )

    def test_daily_dd_violation(self):
        cfg = self.base_config()
        engine = RiskEngine(cfg)
        acc = self.base_account()
        acc.equity = 94000
        snap = self.base_snapshot(datetime.utcnow())

        with self.assertRaises(RuleViolation):
            engine.validate_trade(acc, snap, Signal("BUY", "ok"), [])

    def test_valid_trade_passes(self):
        cfg = self.base_config()
        engine = RiskEngine(cfg)
        acc = self.base_account()
        now = datetime.utcnow()
        snap = self.base_snapshot(now)

        engine.validate_trade(acc, snap, Signal("BUY", "ok"), [now.replace(year=now.year + 1)])


if __name__ == "__main__":
    unittest.main()
