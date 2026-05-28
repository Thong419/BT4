from __future__ import annotations

from app.clients.grpc_intent_client import GrpcIntentClient
from app.core.schemas import IntentResult


class IntentNode:
    def __init__(self, client: GrpcIntentClient) -> None:
        self._client = client

    def run(self, message: str) -> IntentResult:
        return self._client.classify(message)