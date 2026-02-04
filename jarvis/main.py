"""CLI entrypoint for the Jarvis assistant."""

from __future__ import annotations

import argparse
import logging

from jarvis.config import load_config
from jarvis.logging_utils import configure_logging
from jarvis.memory import MemoryStore, format_memory_summary
from jarvis.response import generate_response
from jarvis.runtime import RuntimeState
from jarvis.safety import SafetyChecker
from jarvis.voice import speak_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Jarvis assistant CLI starter.",
    )
    parser.add_argument(
        "--name",
        default=None,
        help="Override assistant name (default: from config).",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print version info and exit.",
    )
    parser.add_argument(
        "message",
        nargs="*",
        help="Message to send to Jarvis.",
    )
    parser.add_argument(
        "--mode",
        default=None,
        choices=[
            "assistant",
            "trading",
            "automation",
            "focus",
            "study",
        ],
        help="Force a specific interaction mode.",
    )
    parser.add_argument(
        "--remember",
        action="store_true",
        help="Remember the current message (if memory enabled).",
    )
    parser.add_argument(
        "--speak",
        action="store_true",
        help="Speak the response aloud (requires voice enabled).",
    )
    return parser


def run_cli(args: argparse.Namespace) -> int:
    config = load_config()
    configure_logging(config.log_level)

    logger = logging.getLogger("jarvis")
    assistant_name = args.name or config.assistant_name
    memory = MemoryStore(config.memory_path, enabled=config.memory_enabled)
    safety = SafetyChecker()
    runtime = RuntimeState(
        wake_word=config.wake_word,
        hotkey=config.hotkey,
        locale=config.locale,
        mode=args.mode or "assistant",
    )

    if args.version:
        print(f"{assistant_name} (env={config.environment})")
        return 0

    if args.message:
        user_message = " ".join(args.message)
        logger.info("Received message: %s", user_message)
        if args.remember:
            memory.add_entry(user_message)
        response = generate_response(
            user_message=user_message,
            assistant_name=assistant_name,
            config=config,
            memory=memory,
            runtime=runtime,
            safety=safety,
        )
        print(response)
        if args.speak:
            voice_result = speak_text(response, config)
            if not voice_result.success:
                print(f"{assistant_name}: {voice_result.message}")
        return 0

    memory_summary = format_memory_summary(memory)
    if memory_summary:
        print(memory_summary)
    print(
        f"{assistant_name}: Main ready hoon. "
        "Ek message pass karo jaise: python -m jarvis.main Hello"
    )
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return run_cli(args)


if __name__ == "__main__":
    raise SystemExit(main())
