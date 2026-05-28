# Backend API Gateway

This service exposes the FastAPI gateway for the banking assistant workflow.

## Run locally

```bash
python -m pip install -r requirements.txt
python run.py
```

## Endpoints

- `GET /health`
- `GET /config`
- `POST /run-agent`
