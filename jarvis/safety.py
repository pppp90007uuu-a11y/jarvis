"""Safety checks for permission-bound actions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass
class SafetyChecker:
    """Encapsulates simple permission rules."""

    destructive_keywords = (
        "delete",
        "format",
        "remove",
        "shutdown",
        "restart",
        "wipe",
    )

    def check_screen_permission(self, command: str) -> Tuple[bool, str]:
        if "jarvis screen dekho" in command.lower():
            return True, "Screen access permission granted."
        return False, "Screen access ke liye 'Jarvis screen dekho' kehna zaroori hai."

    def requires_confirmation(self, command: str) -> bool:
        lowered = command.lower()
        return any(keyword in lowered for keyword in self.destructive_keywords)
