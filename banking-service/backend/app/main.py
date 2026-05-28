from __future__ import annotations

from fastapi import FastAPI, HTTPException

from app.agent.orchestrator import BankingOrchestrator
from app.core.schemas import AgentRequest, ConfigResponse, HealthResponse, RunAgentResponse
from app.core.settings import Settings, get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version=settings.app_version)
    app.state.settings = settings
    app.state.orchestrator = BankingOrchestrator(settings)

    @app.get("/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        return HealthResponse(status="ok", service=settings.app_name)

    @app.get("/config", response_model=ConfigResponse)
    def config() -> ConfigResponse:
        return ConfigResponse(
            settings={
                "app_name": settings.app_name,
                "app_version": settings.app_version,
                "backend_host": settings.backend_host,
                "backend_port": settings.backend_port,
                "intent_service_host": settings.intent_service_host,
                "intent_service_port": settings.intent_service_port,
                "ollama_base_url": settings.ollama_base_url,
                "ollama_model": settings.ollama_model,
                "intent_model_name": settings.intent_model_name,
            },
            dependencies={
                "grpc_intent_service": f"{settings.intent_service_host}:{settings.intent_service_port}",
                "ollama_base_url": settings.ollama_base_url,
            },
        )

    @app.post("/run-agent", response_model=RunAgentResponse)
    def run_agent(payload: AgentRequest) -> RunAgentResponse:
        try:
            orchestrator: BankingOrchestrator = app.state.orchestrator
            return orchestrator.run(payload.message)
        except Exception as exc:  # noqa: BLE001
            raise HTTPException(status_code=500, detail=f"Agent workflow failed: {exc}") from exc

    return app


app = create_app()