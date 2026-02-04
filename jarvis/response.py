"""Response generator for Jarvis assistant."""

from __future__ import annotations

from jarvis.config import AppConfig
from jarvis.memory import MemoryStore
from jarvis.runtime import RuntimeState, run_automation_task, run_utility_action
from jarvis.safety import SafetyChecker


def generate_response(
    user_message: str,
    assistant_name: str,
    config: AppConfig,
    memory: MemoryStore,
    runtime: RuntimeState,
    safety: SafetyChecker,
) -> str:
    lowered = user_message.lower()

    if "jarvis memory clear karo" in lowered:
        memory.clear()
        return "Theek hai, maine memory clear kar di hai."

    if "trading mode" in lowered:
        runtime.update_mode("trading")
        return (
            "Trading mode active. Main charts, indicators, aur news summary me help karunga. "
            "Final decision aapka hoga."
        )

    if "automation mode" in lowered:
        runtime.update_mode("automation")
        return "Automation mode active. Kaun sa task karna hai?"

    if "focus mode" in lowered:
        runtime.update_mode("focus")
        return "Focus mode active. Distracting notifications ko limit karenge."

    if "study mode" in lowered:
        runtime.update_mode("study")
        return "Study mode active. Aaj ka study plan batao."

    if "jarvis screen dekho" in lowered:
        allowed, message = safety.check_screen_permission(user_message)
        runtime.screen_vision_enabled = allowed
        return message

    if "jarvis camera on karo" in lowered:
        allowed, message = safety.check_camera_permission(user_message)
        runtime.camera_vision_enabled = allowed
        return message

    if "jarvis camera band karo" in lowered:
        runtime.camera_vision_enabled = False
        return "Camera access band kar diya hai."

    if "screen band karo" in lowered:
        runtime.screen_vision_enabled = False
        return "Screen access band kar diya hai."

    if runtime.mode == "trading":
        return (
            "Trading mode ready. Symbol, timeframe, ya indicator batao. "
            "Main sirf analysis aur reminders dunga."
        )

    if runtime.mode == "automation":
        return run_automation_task(user_message)

    if runtime.mode in {"focus", "study"}:
        return (
            f"{runtime.mode.title()} mode active. "
            "Goals aur timers set karne ke liye batayein."
        )

    if "remind" in lowered or "yaad dilao" in lowered:
        if memory.enabled:
            memory.add_entry(user_message)
            return "Noted. Main is reminder ko memory me save kar raha hoon."
        return "Memory disabled hai. Reminder save nahi ho sakta."

    if "calculator" in lowered or "convert" in lowered:
        return run_utility_action(user_message)

    return (
        f"{assistant_name}: Main yahan hoon. "
        "Aap command do, main guide karunga. "
        f"Wake word '{config.wake_word}' hai aur hotkey '{config.hotkey}' set hai. "
        "Agar voice output chahiye to --speak flag use karein."
    )
