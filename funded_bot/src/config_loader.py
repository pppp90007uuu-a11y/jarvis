from pathlib import Path
import json


def load_config(config_path: str) -> dict:
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    required_top_level = ["account", "trading", "sessions", "strategy"]
    for key in required_top_level:
        if key not in data:
            raise ValueError(f"Missing required config section: {key}")

    return data
