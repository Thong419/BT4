from __future__ import annotations

from app.core.schemas import IntentResult, PriorityResult


class PriorityNode:
    def run(self, message: str, intent: IntentResult) -> PriorityResult:
        text = message.lower()
        urgent_terms = ("immediately", "urgent", "asap", "right now", "fraud", "lost", "stolen", "block", "need to block")
        severe_terms = ("fraud", "unauthorized", "stolen", "lost card", "lost my card", "credit card", "security", "scam")

        score = 0.25
        reason_parts: list[str] = []

        if any(term in text for term in severe_terms):
            score += 0.5
            reason_parts.append("Contains high-risk security or fraud language.")

        if any(term in text for term in urgent_terms):
            score += 0.2
            reason_parts.append("Contains urgent timing language.")

        if intent.intent in {"lost_card", "block_card", "fraud_report"}:
            score += 0.2
            reason_parts.append("Intent is security-sensitive.")

        score = min(score, 1.0)
        if score >= 0.8:
            risk_level = "high"
        elif score >= 0.5:
            risk_level = "medium"
        else:
            risk_level = "low"

        reason = " ".join(reason_parts) or "No urgent or sensitive markers were detected."
        return PriorityResult(risk_level=risk_level, score=score, reason=reason)