"""Safety checks for permission-bound actions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass
class SafetyChecker:
    """Encapsulates simple permission rules."""

    def check_screen_permission(self, command: str) -> Tuple[bool, str]:
        if "jarvis screen dekho" in command.lower():
            return True, "Screen access permission granted."
        return False, "Screen access ke liye 'Jarvis screen dekho' kehna zaroori hai."

    def check_camera_permission(self, command: str) -> Tuple[bool, str]:
        if "jarvis camera on karo" in command.lower():
            return True, "Camera access permission granted."
        return False, "Camera access ke liye 'Jarvis camera on karo' kehna zaroori hai."
