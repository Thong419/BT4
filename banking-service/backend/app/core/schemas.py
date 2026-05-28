from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    message: str = Field(..., min_length=1, description="Customer banking message")


class IntentResult(BaseModel):
    intent: str
    confidence: float
    reason: str


class PriorityResult(BaseModel):
    risk_level: str
    score: float
    reason: str


class PolicyResult(BaseModel):
    intent: str
    title: str
    content: str
    required_information: list[str] = Field(default_factory=list)
    next_action: str
    routing_queue: str


class ValidationResult(BaseModel):
    is_valid: bool
    missing_information: list[str] = Field(default_factory=list)
    notes: str = ""


class RunAgentResponse(BaseModel):
    original_message: str
    predicted_intent: str
    confidence: float
    intent_reason: str
    priority_level: str
    risk_level: str
    retrieved_policy_title: str
    retrieved_policy_content: str
    validation_result: ValidationResult
    routing_decision: str
    draft_reply: str
    missing_information: list[str] = Field(default_factory=list)
    next_recommended_action: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class HealthResponse(BaseModel):
    status: str
    service: str


class ConfigResponse(BaseModel):
    settings: dict[str, object]
    dependencies: dict[str, object]