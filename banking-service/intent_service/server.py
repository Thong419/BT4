from __future__ import annotations

from concurrent import futures

import grpc

import intent_service_pb2
import intent_service_pb2_grpc
from app.clients.ollama_client import OllamaClient
from app.core.settings import Settings, get_settings
from app.nodes.intent_node import IntentNode


class IntentServiceServicer(intent_service_pb2_grpc.IntentServiceServicer):
    def __init__(self, node: IntentNode) -> None:
        self._node = node

    def IntentRecognizer(self, request: intent_service_pb2.IntentRequest, context: grpc.ServicerContext) -> intent_service_pb2.IntentResponse:  # noqa: N802
        result = self._node.classify(request.message)
        return intent_service_pb2.IntentResponse(intent=result.intent, confidence=result.confidence, reason=result.reason)


def serve() -> None:
    settings = get_settings()
    node = IntentNode(OllamaClient(settings))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    intent_service_pb2_grpc.add_IntentServiceServicer_to_server(IntentServiceServicer(node), server)
    server.add_insecure_port(f"{settings.grpc_host}:{settings.grpc_port}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()