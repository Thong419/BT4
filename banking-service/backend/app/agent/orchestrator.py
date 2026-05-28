from __future__ import annotations

from dataclasses import dataclass

from app.clients.grpc_intent_client import GrpcIntentClient
from app.clients.ollama_client import OllamaClient
from app.core.schemas import IntentResult, PolicyResult, PriorityResult, RunAgentResponse, ValidationResult
from app.core.settings import Settings
from app.nodes.draft_node import DraftNode
from app.nodes.intent_node import IntentNode
from app.nodes.policy_node import PolicyNode
from app.nodes.priority_node import PriorityNode
from app.nodes.router_node import RouterNode
from app.nodes.validation_node import ValidationNode


@dataclass(slots=True)
class WorkflowArtifacts:
    intent: IntentResult
    priority: PriorityResult
    policy: PolicyResult
    validation: ValidationResult
    routing_decision: str
    draft_reply: str


class BankingOrchestrator:
    def __init__(self, settings: Settings) -> None:
        intent_client = GrpcIntentClient(settings)
        ollama_client = OllamaClient(settings)

        self._intent_node = IntentNode(intent_client)
        self._priority_node = PriorityNode()
        self._policy_node = PolicyNode()
        self._validation_node = ValidationNode()
        self._router_node = RouterNode()
        self._draft_node = DraftNode(ollama_client)
        self._ollama_client = ollama_client

    def run(self, message: str) -> RunAgentResponse:
        artifacts = self._execute(message)
        return RunAgentResponse(
            original_message=message,
            predicted_intent=artifacts.intent.intent,
            confidence=artifacts.intent.confidence,
            intent_reason=artifacts.intent.reason,
            priority_level=artifacts.priority.risk_level,
            risk_level=artifacts.priority.risk_level,
            retrieved_policy_title=artifacts.policy.title,
            retrieved_policy_content=artifacts.policy.content,
            validation_result=artifacts.validation,
            routing_decision=artifacts.routing_decision,
            draft_reply=artifacts.draft_reply,
            missing_information=artifacts.validation.missing_information,
            next_recommended_action=artifacts.policy.next_action,
            metadata={
                "priority_score": artifacts.priority.score,
                "priority_reason": artifacts.priority.reason,
                "policy_queue": artifacts.policy.routing_queue,
                "ollama_enabled": self._ollama_client.is_available(),
            },
        )

    def _execute(self, message: str) -> WorkflowArtifacts:
        intent = self._intent_node.run(message)
        priority = self._priority_node.run(message, intent)
        policy = self._policy_node.run(intent)
        validation = self._validation_node.run(message, policy)
        routing_decision = self._router_node.run(policy, priority, validation)
        draft_reply = self._draft_node.run(message, intent, priority, policy, validation, routing_decision)
        return WorkflowArtifacts(
            intent=intent,
            priority=priority,
            policy=policy,
            validation=validation,
            routing_decision=routing_decision,
            draft_reply=draft_reply,
        )