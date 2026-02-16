import argparse
from datetime import datetime, timedelta

from src.alerts import AlertManager
from src.config_loader import load_config
from src.executor import Executor
from src.models import AccountState, MarketSnapshot
from src.risk_engine import RiskEngine, RuleViolation
from src.strategy import generate_signal


def get_mock_snapshot(now: datetime) -> MarketSnapshot:
    return MarketSnapshot(
        symbol="EURUSD",
        time=now,
        bid=1.0840,
        ask=1.0842,
        spread_points=20,
        slippage_points=5,
        ema_fast=1.0835,
        ema_slow=1.0820,
        atr=0.0012,
        close=1.0841,
        prev_close=1.0838,
    )


def run_once(config: dict, mode: str = "dry-run") -> None:
    risk_engine = RiskEngine(config)
    executor = Executor(mode=mode)
    alerts = AlertManager(config)

    account = AccountState(
        balance=100000,
        equity=99800,
        day_start_balance=100000,
        open_positions=0,
        open_lots=0.0,
    )

    now = datetime.utcnow()
    snapshot = get_mock_snapshot(now)
    news_times = [now + timedelta(minutes=120)]

    signal = generate_signal(snapshot)

    try:
        risk_engine.validate_trade(account, snapshot, signal, news_times)
        plan = risk_engine.build_trade_plan(account, snapshot, signal)
        result = executor.place_order(plan)
        msg = f"ORDER RESULT: {result['status']} | {result['message']}"
        print(msg)
        alerts.send(msg)
    except RuleViolation as e:
        msg = f"TRADE REJECTED: {str(e)}"
        print(msg)
        alerts.send(msg)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--mode", default="dry-run")
    args = parser.parse_args()

    config = load_config(args.config)
    run_once(config, mode=args.mode)


if __name__ == "__main__":
    main()
