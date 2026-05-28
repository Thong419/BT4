from __future__ import annotations

from typing import Protocol

from app.core.schemas import IntentResult


class IntentClient(Protocol):
    def classify(self, message: str) -> IntentResult:
        ...


class TextGenerationClient(Protocol):
    def generate(self, prompt: str, system_prompt: str | None = None) -> str | None:
        ...