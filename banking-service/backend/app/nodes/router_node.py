from __future__ import annotations

from app.core.schemas import PolicyResult, PriorityResult, ValidationResult


class RouterNode:
    def run(self, policy: PolicyResult, priority: PriorityResult, validation: ValidationResult) -> str:
        queue = policy.routing_queue
        if priority.risk_level == "high":
            return f"priority-{queue}"
        if not validation.is_valid and queue != "general-support":
            return f"intake-{queue}"
        return queue