"""Trading assistant helpers (analysis-only, no trade execution)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class TradingPlan:
    symbol: Optional[str]
    timeframe: Optional[str]
    indicators: tuple[str, ...]


DEFAULT_INDICATORS = ("RSI", "MACD", "EMA", "Volume")


def build_trading_plan(symbol: Optional[str], timeframe: Optional[str]) -> TradingPlan:
    return TradingPlan(symbol=symbol, timeframe=timeframe, indicators=DEFAULT_INDICATORS)


def format_trading_brief(plan: TradingPlan) -> str:
    symbol = plan.symbol or "symbol not set"
    timeframe = plan.timeframe or "timeframe not set"
    indicators = ", ".join(plan.indicators)
    return (
        "Trading brief ready. "
        f"Symbol: {symbol}, Timeframe: {timeframe}. "
        f"Indicators: {indicators}. "
        "Main sirf analysis aur education provide karta hoon, trade execute nahi karta."
    )
