"""Runtime state and action helpers for the Jarvis assistant."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class RuntimeState:
    wake_word: str
    hotkey: str
    locale: str
    mode: str
    screen_vision_enabled: bool = False
    pending_action: Optional[str] = None
    trading_symbol: Optional[str] = None
    trading_timeframe: Optional[str] = None
    voice_listen_enabled: bool = False

    def update_mode(self, mode: str) -> None:
        self.mode = mode

    def queue_action(self, action: str) -> None:
        self.pending_action = action

    def clear_pending_action(self) -> None:
        self.pending_action = None

    def update_trading_context(self, symbol: Optional[str], timeframe: Optional[str]) -> None:
        if symbol:
            self.trading_symbol = symbol
        if timeframe:
            self.trading_timeframe = timeframe

    def set_voice_listen(self, enabled: bool) -> None:
        self.voice_listen_enabled = enabled


def run_automation_task(command: str) -> str:
    """Stub for automation tasks that require explicit permission."""
    return (
        "Automation task queue ready hai. "
        f"Command receive hua: {command}. "
        "Critical actions se pehle confirmation liya jaayega."
    )


def run_utility_action(command: str) -> str:
    """Stub for quick utilities like calculator or conversions."""
    return (
        "Utility action ready hai. "
        f"Input receive hua: {command}. "
        "Isko execute karne se pehle context confirm karunga."
    )
