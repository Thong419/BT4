from __future__ import annotations

from dataclasses import dataclass

from app.clients.ollama_client import OllamaClient
from app.core.schemas import IntentClassificationResult


@dataclass(slots=True)
class RuleBasedIntentClassifier:
    intents: dict[str, tuple[str, ...]]

    @classmethod
    def default(cls) -> "RuleBasedIntentClassifier":
        return cls(
            intents={
                "lost_card": (
                    "lost card",
                    "lost my card",
                    "lost my credit card",
                    "lost my debit card",
                    "missing card",
                    "stolen card",
                ),
                "block_card": (
                    "block card",
                    "block it",
                    "need to block",
                    "freeze card",
                    "card blocked",
                    "stop my card",
                ),
                "loan_inquiry": ("loan", "mortgage", "borrow", "credit line"),
                "balance_check": ("balance", "account balance", "how much money", "check my balance"),
                "money_transfer": ("transfer", "send money", "wire", "payment"),
                "fraud_report": ("fraud", "unauthorized", "scam", "suspicious", "chargeback"),
                "account_update": ("update address", "change phone", "change email", "account update"),
            }
        )

    def classify(self, message: str) -> IntentClassificationResult:
        text = message.lower()
        for intent, keywords in self.intents.items():
            if any(keyword in text for keyword in keywords):
                return IntentClassificationResult(intent=intent, confidence=0.85, reason=f"Matched keywords for {intent.replace('_', ' ')}.")
        return IntentClassificationResult(intent="general_support", confidence=0.54, reason="No specific intent keywords were detected.")


class IntentNode:
    def __init__(self, ollama_client: OllamaClient) -> None:
        self._ollama_client = ollama_client
        self._rules = RuleBasedIntentClassifier.default()

    def classify(self, message: str) -> IntentClassificationResult:
        rule_result = self._rules.classify(message)
        if rule_result.intent != "general_support" and rule_result.confidence >= 0.8:
            return rule_result

        if self._ollama_client.is_available():
            result = self._ollama_client.classify(message)
            if result is not None:
                return result
        return rule_result
