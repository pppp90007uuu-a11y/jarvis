"""Text-to-speech helpers for Jarvis."""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass

from jarvis.config import AppConfig


@dataclass
class VoiceResult:
    success: bool
    message: str


def speak_text(text: str, config: AppConfig) -> VoiceResult:
    if not config.voice_enabled:
        return VoiceResult(False, "Voice disabled hai. JARVIS_VOICE_ENABLED=true set karein.")

    engine = config.tts_engine.lower()
    voice = config.tts_voice

    if engine == "say":
        if not shutil.which("say"):
            return VoiceResult(False, "System me 'say' command available nahi hai.")
        command = ["say", "-v", voice, text]
    else:
        if not shutil.which("espeak"):
            return VoiceResult(False, "System me 'espeak' command available nahi hai.")
        command = ["espeak", "-v", voice, text]

    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        details = result.stderr.strip() or "Unknown error"
        return VoiceResult(False, f"TTS failed: {details}")
    return VoiceResult(True, "Voice output successful.")
