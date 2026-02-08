"""Response generator for Jarvis assistant."""

from __future__ import annotations

from jarvis.config import AppConfig
from jarvis.memory import MemoryStore
from jarvis.runtime import RuntimeState, run_automation_task, run_utility_action
from jarvis.safety import SafetyChecker
from jarvis.trading import build_trading_plan, format_trading_brief
from jarvis.voice_input import build_voice_setup_instructions, check_voice_dependencies


def generate_response(
    user_message: str,
    assistant_name: str,
    config: AppConfig,
    memory: MemoryStore,
    runtime: RuntimeState,
    safety: SafetyChecker,
) -> str:
    lowered = user_message.lower()

    if "cancel" in lowered:
        runtime.clear_pending_action()
        return "Theek hai, pending action cancel kar diya hai."

    if runtime.pending_action and "confirm" in lowered:
        action = runtime.pending_action
        runtime.clear_pending_action()
        return (
            "Confirmation mil gaya. "
            f"Action '{action}' ko execute karne se pehle main phir se steps share karunga."
        )

    if runtime.pending_action:
        return (
            "Aapka last action critical hai. "
            "Confirm karne ke liye 'confirm' likhen ya cancel karne ke liye 'cancel' bolein."
        )

    if config.require_wake_word and runtime.mode == "assistant":
        if config.wake_word.lower() not in lowered:
            return (
                f"{assistant_name}: Main idle hoon. "
                f"Activate karne ke liye wake word '{config.wake_word}' use karein "
                "ya hotkey trigger karein."
            )

    if "jarvis help" in lowered or "help" in lowered:
        return (
            "Commands: 'Jarvis screen dekho', "
            "'trading mode', 'automation mode', 'focus mode', 'study mode', "
            "'Jarvis memory clear karo', 'Jarvis status'. "
            "Voice ke liye CLI me --speak flag use karein."
        )

    if "jarvis status" in lowered:
        memory_state = "on" if memory.enabled else "off"
        voice_state = "on" if config.voice_enabled else "off"
        listen_state = "on" if runtime.voice_listen_enabled else "off"
        return (
            "Status: "
            f"mode={runtime.mode}, memory={memory_state}, voice={voice_state}, "
            f"wake_word='{config.wake_word}', hotkey='{config.hotkey}', "
            f"voice_listen={listen_state}."
        )

    if "jarvis memory clear karo" in lowered:
        memory.clear()
        return "Theek hai, maine memory clear kar di hai."

    if "jarvis listen on" in lowered:
        status = check_voice_dependencies()
        runtime.set_voice_listen(status.ok)
        return build_voice_setup_instructions(status)

    if "jarvis listen off" in lowered:
        runtime.set_voice_listen(False)
        return "Voice listening band kar diya hai."

    if "trading mode" in lowered:
        runtime.update_mode("trading")
        return (
            "Trading mode active. Main charts, indicators, aur news summary me help karunga. "
            "Final decision aapka hoga."
        )

    if "iron man mode" in lowered or "ironman mode" in lowered:
        runtime.update_mode("ironman")
        return (
            "Iron Man mode active. Main crisp status updates, smart summaries, "
            "aur mission-style task breakdown dunga. Safety aur consent rules follow honge."
        )

    if "set symbol" in lowered or "symbol" in lowered:
        parts = user_message.split()
        symbol = parts[-1] if parts else None
        runtime.update_trading_context(symbol=symbol, timeframe=None)
        return f"Trading symbol set kiya: {runtime.trading_symbol}."

    if "set timeframe" in lowered or "timeframe" in lowered:
        parts = user_message.split()
        timeframe = parts[-1] if parts else None
        runtime.update_trading_context(symbol=None, timeframe=timeframe)
        return f"Trading timeframe set kiya: {runtime.trading_timeframe}."

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

    if "screen band karo" in lowered:
        runtime.screen_vision_enabled = False
        return "Screen access band kar diya hai."

    if "voice control" in lowered or "bol ke control" in lowered:
        status = check_voice_dependencies()
        return (
            "Voice control opt-in hai aur hamesha-on mode allowed nahi hai. "
            f"{build_voice_setup_instructions(status)}"
        )

    if safety.requires_confirmation(user_message):
        runtime.queue_action(user_message)
        return (
            "Yeh action sensitive hai. "
            "Confirm karne ke liye 'confirm' likhen ya 'cancel' bolein."
        )

    if runtime.mode == "trading":
        plan = build_trading_plan(runtime.trading_symbol, runtime.trading_timeframe)
        return format_trading_brief(plan)

    if runtime.mode == "automation":
        return run_automation_task(user_message)

    if runtime.mode in {"focus", "study"}:
        return (
            f"{runtime.mode.title()} mode active. "
            "Goals aur timers set karne ke liye batayein."
        )

    if runtime.mode == "ironman":
        return (
            "Iron Man mode ready. Mission do: task list, priority, aur desired outcome. "
            "Main step-by-step execution plan banaunga."
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
