import json
from urllib import request


class AlertManager:
    def __init__(self, config: dict):
        alerts = config.get("alerts", {})
        self.enabled = alerts.get("telegram_enabled", False)
        self.token = alerts.get("telegram_bot_token", "")
        self.chat_id = alerts.get("telegram_chat_id", "")

    def send(self, message: str) -> None:
        if not self.enabled:
            return
        if not self.token or not self.chat_id or "REPLACE_ME" in (self.token, self.chat_id):
            return

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = json.dumps({"chat_id": self.chat_id, "text": message}).encode("utf-8")
        req = request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        try:
            request.urlopen(req, timeout=10)
        except Exception:
            # Alert path should never crash trading loop.
            pass
