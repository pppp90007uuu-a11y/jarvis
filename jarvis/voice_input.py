"""Voice command setup helpers (optional local dependencies)."""

from __future__ import annotations

import importlib.util
from dataclasses import dataclass


@dataclass
class VoiceDependencyStatus:
    ok: bool
    missing: tuple[str, ...]


REQUIRED_MODULES = ("speech_recognition", "pyaudio", "pyttsx3")


def check_voice_dependencies() -> VoiceDependencyStatus:
    missing = tuple(
        module for module in REQUIRED_MODULES if importlib.util.find_spec(module) is None
    )
    return VoiceDependencyStatus(ok=len(missing) == 0, missing=missing)


def build_voice_setup_instructions(status: VoiceDependencyStatus) -> str:
    if status.ok:
        return "Voice dependencies ready hain. Aap 'Jarvis listen on' bol kar start kar sakte ho."
    missing_list = ", ".join(status.missing)
    return (
        "Voice control ke liye local dependencies install karni hongi. "
        f"Missing: {missing_list}. "
        "Install command: pip install speechrecognition pyttsx3 pyaudio"
    )
