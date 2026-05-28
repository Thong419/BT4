from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests

from app.core.schemas import IntentClassificationResult
from app.core.settings import Settings


@dataclass(slots=True)
class OllamaClient:
    settings: Settings

    def is_available(self) -> bool:
        try:
            response = requests.get(f"{self.settings.ollama_base_url}/api/tags", timeout=3)
            return response.ok
        except requests.RequestException:
            return False

    def classify(self, message: str) -> IntentClassificationResult | None:
        prompt = (
            "Classify the customer message into one of these banking intents: "
            "lost_card, block_card, loan_inquiry, balance_check, money_transfer, fraud_report, account_update, general_support. "
            "Return JSON with keys intent, confidence, reason. "
            f"Message: {message}"
        )
        payload: dict[str, Any] = {
            "model": self.settings.intent_model_name,
            "stream": False,
            "messages": [
                {"role": "system", "content": "You are a strict banking intent classifier."},
                {"role": "user", "content": prompt},
            ],
        }
        try:
            response = requests.post(f"{self.settings.ollama_base_url}/api/chat", json=payload, timeout=self.settings.request_timeout_seconds)
            response.raise_for_status()
            data = response.json()
            message_obj = data.get("message", {}) if isinstance(data, dict) else {}
            content = message_obj.get("content") if isinstance(message_obj, dict) else None
            if not isinstance(content, str):
                return None
            return self._parse_model_output(content)
        except requests.RequestException:
            return None

    def _parse_model_output(self, content: str) -> IntentClassificationResult | None:
        import json

        stripped = content.strip()
        if stripped.startswith("```"):
            stripped = stripped.strip("`")
        try:
            data = json.loads(stripped)
            intent = str(data.get("intent", "general_support"))
            confidence = float(data.get("confidence", 0.6))
            reason = str(data.get("reason", "Ollama classification result."))
            return IntentClassificationResult(intent=intent, confidence=max(0.0, min(1.0, confidence)), reason=reason)
        except Exception:
            return None