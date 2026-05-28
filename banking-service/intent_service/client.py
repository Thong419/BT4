from __future__ import annotations

import argparse

import grpc

import intent_service_pb2
import intent_service_pb2_grpc


def main() -> None:
    parser = argparse.ArgumentParser(description="Call the banking intent gRPC service")
    parser.add_argument("message", help="Customer message to classify")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", default="50051")
    args = parser.parse_args()

    target = f"{args.host}:{args.port}"
    with grpc.insecure_channel(target) as channel:
        stub = intent_service_pb2_grpc.IntentServiceStub(channel)
        response = stub.IntentRecognizer(intent_service_pb2.IntentRequest(message=args.message), timeout=10)
        print({"intent": response.intent, "confidence": response.confidence, "reason": response.reason})


if __name__ == "__main__":
    main()