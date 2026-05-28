from __future__ import annotations

from app.core.schemas import IntentResult, PolicyResult
from app.data.policies import get_policy


class PolicyNode:
    def run(self, intent: IntentResult) -> PolicyResult:
        policy = get_policy(intent.intent)
        return PolicyResult(
            intent=policy.intent,
            title=policy.title,
            content=policy.content,
            required_information=list(policy.required_information),
            next_action=policy.next_action,
            routing_queue=policy.routing_queue,
        )