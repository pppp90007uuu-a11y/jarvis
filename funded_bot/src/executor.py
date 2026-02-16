from src.models import TradePlan


class Executor:
    """
    Starter executor.
    Replace with MT5 order_send/order_check implementation in production.
    """

    def __init__(self, mode: str = "dry-run"):
        self.mode = mode

    def place_order(self, plan: TradePlan) -> dict:
        if self.mode == "dry-run":
            return {
                "status": "ok",
                "mode": self.mode,
                "message": f"[DRY-RUN] {plan.side} {plan.symbol} {plan.lot_size} lot @ {plan.entry}",
            }

        # Real bridge placeholder
        return {
            "status": "error",
            "mode": self.mode,
            "message": "Real MT5 bridge not implemented yet.",
        }
