from __future__ import annotations

from typing import Protocol

from app.core.schemas import IntentClassificationResult


class IntentClassifier(Protocol):
    def classify(self, message: str) -> IntentClassificationResult:
        ...