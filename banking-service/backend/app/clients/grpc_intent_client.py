from __future__ import annotations

from dataclasses import dataclass

import grpc

from app.core.schemas import IntentResult
from app.core.settings import Settings
from app.data.policies import INTENT_ALIASES

import intent_service_pb2
import intent_service_pb2_grpc


@dataclass(slots=True)
class LocalIntentHeuristics:
    keywords: dict[str, tuple[str, ...]] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.keywords is None:
            self.keywords = {
                "lost_card": (
                    "lost card",
                    "lost my card",
                    "lost my credit card",
                    "lost my debit card",
                    "misplaced card",
                    "stolen card",
                    "missing card",
                ),
                "block_card": (
                    "block card",
                    "block it",
                    "need to block",
                    "freeze card",
                    "disable card",
                    "card blocked",
                ),
                "loan_inquiry": ("loan", "mortgage", "credit line", "borrow"),
                "balance_check": ("balance", "how much money", "account balance"),
                "money_transfer": ("transfer", "send money", "wire", "pay someone"),
                "fraud_report": ("fraud", "scam", "unauthorized", "chargeback", "suspicious"),
                "account_update": ("update address", "change phone", "profile update", "change email"),
            }

    def classify(self, message: str) -> IntentResult:
        text = message.lower()
        for intent, terms in self.keywords.items():
            if any(term in text for term in terms):
                reason = f"Matched keywords for {intent.replace('_', ' ')}."
                return IntentResult(intent=intent, confidence=0.84, reason=reason)
        return IntentResult(intent="general_support", confidence=0.52, reason="No strong banking keyword match was found.")


class GrpcIntentClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._heuristics = LocalIntentHeuristics()

    def classify(self, message: str) -> IntentResult:
        target = f"{self._settings.intent_service_host}:{self._settings.intent_service_port}"
        try:
            with grpc.insecure_channel(target) as channel:
                stub = intent_service_pb2_grpc.IntentServiceStub(channel)
                request = intent_service_pb2.IntentRequest(message=message)
                response = stub.IntentRecognizer(request, timeout=self._settings.request_timeout_seconds)
                normalized = INTENT_ALIASES.get(response.intent, response.intent)
                confidence = max(0.0, min(1.0, float(response.confidence)))
                return IntentResult(intent=normalized, confidence=confidence, reason=response.reason or "gRPC intent service response received.")
        except Exception:
            fallback = self._heuristics.classify(message)
            fallback.reason = "gRPC intent service unavailable; local fallback classification used."
            return fallback
