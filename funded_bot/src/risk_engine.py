from datetime import datetime, timedelta
from src.models import AccountState, MarketSnapshot, Signal, TradePlan


class RuleViolation(Exception):
    pass


class RiskEngine:
    def __init__(self, config: dict):
        self.config = config

    def _daily_drawdown_pct(self, account: AccountState) -> float:
        if account.day_start_balance <= 0:
            return 0.0
        return max(0.0, (account.day_start_balance - account.equity) / account.day_start_balance * 100)

    def _overall_drawdown_pct(self, account: AccountState) -> float:
        starting_balance = self.config["account"]["starting_balance"]
        if starting_balance <= 0:
            return 0.0
        return max(0.0, (starting_balance - account.equity) / starting_balance * 100)

    def _is_news_blocked(self, now: datetime, high_impact_news_times: list[datetime]) -> bool:
        news_cfg = self.config.get("news_filter", {})
        if not news_cfg.get("enabled", False):
            return False

        before = timedelta(minutes=news_cfg.get("block_before_minutes", 30))
        after = timedelta(minutes=news_cfg.get("block_after_minutes", 30))
        for t in high_impact_news_times:
            if t - before <= now <= t + after:
                return True
        return False

    def _is_session_allowed(self, now: datetime) -> bool:
        windows = self.config["sessions"].get("allowed_windows", [])
        current = now.strftime("%H:%M")
        for w in windows:
            if w["start"] <= current <= w["end"]:
                return True
        return False

    def validate_trade(
        self,
        account: AccountState,
        snapshot: MarketSnapshot,
        signal: Signal,
        high_impact_news_times: list[datetime],
    ) -> None:
        if signal.side == "FLAT":
            raise RuleViolation("No trade signal")

        if account.disabled:
            raise RuleViolation("Trading disabled due to prior hard violation")

        daily_dd = self._daily_drawdown_pct(account)
        if daily_dd >= self.config["account"]["max_daily_drawdown_pct"]:
            raise RuleViolation("Max daily drawdown hit")

        overall_dd = self._overall_drawdown_pct(account)
        if overall_dd >= self.config["account"]["max_overall_drawdown_pct"]:
            account.disabled = True
            raise RuleViolation("Max overall drawdown hit; disabling trading")

        if snapshot.spread_points > self.config["trading"]["max_spread_points"]:
            raise RuleViolation("Spread too high")

        if snapshot.slippage_points > self.config["trading"]["max_slippage_points"]:
            raise RuleViolation("Slippage too high")

        if self._is_news_blocked(snapshot.time, high_impact_news_times):
            raise RuleViolation("Within blocked news window")

        if not self._is_session_allowed(snapshot.time):
            raise RuleViolation("Outside allowed session")

        if account.open_positions >= self.config["account"]["max_open_positions"]:
            raise RuleViolation("Max open positions reached")

        if account.open_lots >= self.config["account"]["max_total_exposure_lots"]:
            raise RuleViolation("Max total exposure reached")

    def build_trade_plan(self, account: AccountState, snapshot: MarketSnapshot, signal: Signal) -> TradePlan:
        risk_pct = self.config["trading"]["risk_per_trade_pct"]
        rr_ratio = self.config["trading"]["rr_ratio"]

        risk_amount = account.balance * (risk_pct / 100)
        sl_distance = max(snapshot.atr, 0.0001)

        # Simplified fx sizing approximation for starter use.
        lot_size = round(risk_amount / (sl_distance * 100000), 2)
        lot_size = min(lot_size, self.config["account"]["max_lot_size"])

        entry = snapshot.ask if signal.side == "BUY" else snapshot.bid
        sl = entry - sl_distance if signal.side == "BUY" else entry + sl_distance
        tp_distance = sl_distance * rr_ratio
        tp = entry + tp_distance if signal.side == "BUY" else entry - tp_distance

        return TradePlan(
            symbol=snapshot.symbol,
            side=signal.side,
            lot_size=max(lot_size, 0.01),
            entry=entry,
            sl=sl,
            tp=tp,
            risk_pct=risk_pct,
        )
