"""Configuration handling for the Jarvis assistant."""

from __future__ import annotations

from dataclasses import dataclass
from os import getenv
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class AppConfig:
    """Configuration values for the assistant."""

    assistant_name: str
    environment: str
    log_level: str
    wake_word: str
    hotkey: str
    locale: str
    memory_path: Path
    memory_enabled: bool
    voice_enabled: bool
    tts_engine: str
    tts_voice: str
    require_wake_word: bool


def load_config() -> AppConfig:
    """Load config from environment variables (supports .env)."""
    load_dotenv()

    memory_enabled = getenv("JARVIS_MEMORY_ENABLED", "true").lower() in {
        "1",
        "true",
        "yes",
    }
    default_memory_path = Path(getenv("JARVIS_MEMORY_PATH", ".jarvis_memory.json"))
    voice_enabled = getenv("JARVIS_VOICE_ENABLED", "false").lower() in {
        "1",
        "true",
        "yes",
    }
    require_wake_word = getenv("JARVIS_REQUIRE_WAKE_WORD", "true").lower() in {
        "1",
        "true",
        "yes",
    }

    return AppConfig(
        assistant_name=getenv("JARVIS_NAME", "Jarvis"),
        environment=getenv("JARVIS_ENV", "development"),
        log_level=getenv("JARVIS_LOG_LEVEL", "INFO"),
        wake_word=getenv("JARVIS_WAKE_WORD", "Jarvis"),
        hotkey=getenv("JARVIS_HOTKEY", "Ctrl+Shift+J"),
        locale=getenv("JARVIS_LOCALE", "hi-IN"),
        memory_path=default_memory_path,
        memory_enabled=memory_enabled,
        voice_enabled=voice_enabled,
        tts_engine=getenv("JARVIS_TTS_ENGINE", "espeak"),
        tts_voice=getenv("JARVIS_TTS_VOICE", "hi"),
        require_wake_word=require_wake_word,
    )
