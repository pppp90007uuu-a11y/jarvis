"""Runtime state and action helpers for the Jarvis assistant."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RuntimeState:
    wake_word: str
    hotkey: str
    locale: str
    mode: str
    screen_vision_enabled: bool = False
    camera_vision_enabled: bool = False

    def update_mode(self, mode: str) -> None:
        self.mode = mode


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
