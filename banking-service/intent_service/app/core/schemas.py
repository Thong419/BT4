from __future__ import annotations

from pydantic import BaseModel


class IntentClassificationResult(BaseModel):
    intent: str
    confidence: float
    reason: str