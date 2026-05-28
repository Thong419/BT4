from __future__ import annotations

from app.clients.ollama_client import OllamaClient
from app.core.schemas import IntentResult, PolicyResult, PriorityResult, ValidationResult


class DraftNode:
    def __init__(self, client: OllamaClient) -> None:
        self._client = client

    def run(
        self,
        message: str,
        intent: IntentResult,
        priority: PriorityResult,
        policy: PolicyResult,
        validation: ValidationResult,
        routing_decision: str,
    ) -> str:
        prompt = (
            "Compose a concise customer-facing banking support reply. "
            "Be calm, helpful, and mention next steps clearly.\n\n"
            f"Customer message: {message}\n"
            f"Predicted intent: {intent.intent}\n"
            f"Priority: {priority.risk_level}\n"
            f"Policy summary: {policy.content}\n"
            f"Missing information: {', '.join(validation.missing_information) or 'none'}\n"
            f"Routing decision: {routing_decision}\n"
            f"Recommended action: {policy.next_action}"
        )
        draft = self._client.generate(prompt, system_prompt="You are a customer service assistant for a banking platform.")
        if draft:
            return draft

        missing = f" Please provide {', '.join(validation.missing_information)}." if validation.missing_information else ""
        return (
            f"Thanks for contacting us about your {intent.intent.replace('_', ' ')} request. "
            f"{policy.content} {policy.next_action}{missing}"
        ).strip()