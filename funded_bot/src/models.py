from dataclasses import dataclass
from datetime import datetime


@dataclass
class MarketSnapshot:
    symbol: str
    time: datetime
    bid: float
    ask: float
    spread_points: float
    slippage_points: float
    ema_fast: float
    ema_slow: float
    atr: float
    close: float
    prev_close: float


@dataclass
class AccountState:
    balance: float
    equity: float
    day_start_balance: float
    open_positions: int
    open_lots: float
    disabled: bool = False


@dataclass
class Signal:
    side: str  # BUY | SELL | FLAT
    reason: str


@dataclass
class TradePlan:
    symbol: str
    side: str
    lot_size: float
    entry: float
    sl: float
    tp: float
    risk_pct: float
