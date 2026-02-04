"""Logging helpers."""

from __future__ import annotations

import logging


def configure_logging(log_level: str) -> None:
    """Configure root logging for the app."""
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
