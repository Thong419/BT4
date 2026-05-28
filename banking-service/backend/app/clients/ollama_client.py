from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests

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

    def generate(self, prompt: str, system_prompt: str | None = None) -> str | None:
        payload: dict[str, Any] = {
            "model": self.settings.ollama_model,
            "stream": False,
            "messages": [
                {"role": "system", "content": system_prompt or "You are a helpful banking assistant."},
                {"role": "user", "content": prompt},
            ],
        }
        try:
            response = requests.post(f"{self.settings.ollama_base_url}/api/chat", json=payload, timeout=self.settings.request_timeout_seconds)
            response.raise_for_status()
            data = response.json()
            message = data.get("message", {}) if isinstance(data, dict) else {}
            content = message.get("content") if isinstance(message, dict) else None
            return content.strip() if isinstance(content, str) and content.strip() else None
        except requests.RequestException:
            return None