from __future__ import annotations

from dataclasses import asdict, dataclass
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "banking-service")
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    backend_host: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    backend_port: int = int(os.getenv("BACKEND_PORT", "8000"))
    intent_service_host: str = os.getenv("INTENT_SERVICE_HOST", "localhost")
    intent_service_port: int = int(os.getenv("INTENT_SERVICE_PORT", "50051"))
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "gpt-oss:20b")
    intent_model_name: str = os.getenv("INTENT_MODEL_NAME", "gpt-oss:20b")
    request_timeout_seconds: float = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "15"))

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def get_settings() -> Settings:
    return Settings()