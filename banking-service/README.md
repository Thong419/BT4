# Banking AI Agent

This project deploys a banking support AI agent with a FastAPI gateway, a gRPC intent classification microservice, and a Streamlit frontend.

## Architecture

The system is split into three containers:

- `backend`: FastAPI API gateway that runs the workflow nodes and exposes `/health`, `/config`, and `/run-agent`.
- `intent-service`: Independent gRPC service that classifies banking intent and falls back to deterministic rules when Ollama is unavailable.
- `frontend`: Streamlit UI for entering customer messages and viewing the structured workflow output.

The backend calls the intent service over gRPC. Both the backend and the intent service can call Ollama over HTTP when it is available, but they both remain functional if Ollama is down.

## Repository Layout

- `backend/`: FastAPI gateway, workflow nodes, policy data, and backend Dockerfile.
- `intent_service/`: gRPC service, proto definition, intent logic, and build tooling.
- `frontend/`: Streamlit UI and frontend Dockerfile.
- `docker-compose.yml`: Orchestrates the three services.

## gRPC Code Generation

The intent service proto is defined in `intent_service/intent_service.proto`.

Generate the Python gRPC code with:

```bash
cd intent_service
make
```

This produces `intent_service_pb2.py` and `intent_service_pb2_grpc.py` in the `intent_service/` directory.

## Ollama Setup

The default model is `gpt-oss:20b`.

Run Ollama on your host machine and pull the model:

```bash
ollama serve
ollama pull gpt-oss:20b
```

If you run the project with Docker Desktop and Ollama on the host, the containers use `http://host.docker.internal:11434` by default.

## Run with Docker Compose

From the `banking-service` directory:

```bash
docker compose up --build
```

Services and ports:

- Backend: `http://localhost:8000`
- gRPC intent service: `localhost:50051`
- Frontend: `http://localhost:8501`

## Sample API Request

```bash
curl -X POST http://localhost:8000/run-agent \
  -H "Content-Type: application/json" \
  -d '{"message":"I lost my credit card and need to block it immediately"}'
```

## Expected Response Shape

```json
{
  "original_message": "I lost my credit card and need to block it immediately",
  "predicted_intent": "lost_card",
  "confidence": 0.84,
  "intent_reason": "Matched keywords for lost card.",
  "priority_level": "high",
  "risk_level": "high",
  "retrieved_policy_title": "Lost Card / Emergency Card Freeze",
  "retrieved_policy_content": "Immediately freeze the card...",
  "validation_result": {
    "is_valid": false,
    "missing_information": ["card last 4 digits"],
    "notes": "Additional details are needed before a final action can be completed."
  },
  "routing_decision": "priority-card-services",
  "draft_reply": "...",
  "missing_information": ["card last 4 digits"],
  "next_recommended_action": "Freeze the card and open a card replacement request."
}
```

## Troubleshooting

- If Ollama is unreachable, confirm the host service is running and that `OLLAMA_BASE_URL` points to `http://host.docker.internal:11434` when using Docker Desktop.
- If gRPC classification fails, check that the `intent-service` container is healthy and listening on port `50051`.
- If the frontend cannot reach the backend, confirm `API_BASE_URL` is set to `http://backend:8000` inside Compose or `http://localhost:8000` when running locally.
- If `docker compose` cannot resolve `host.docker.internal`, keep the `extra_hosts` entry in the compose file.

## Video Demo Link

https://drive.google.com/file/d/11AkRt32ek5w04qDUbw4TuHJ1t4yEx8cg/view?usp=sharing
