from __future__ import annotations

from dataclasses import asdict, dataclass
import os


@dataclass(frozen=True)
class Settings:
    service_name: str = os.getenv("SERVICE_NAME", "intent-service")
    grpc_host: str = os.getenv("GRPC_HOST", "0.0.0.0")
    grpc_port: int = int(os.getenv("GRPC_PORT", "50051"))
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    intent_model_name: str = os.getenv("INTENT_MODEL_NAME", "gpt-oss:20b")
    request_timeout_seconds: float = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "15"))

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def get_settings() -> Settings:
    return Settings()