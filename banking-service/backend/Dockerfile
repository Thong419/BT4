FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    make \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN python -m pip install --no-cache-dir --timeout 120 --retries 10 -r /app/requirements.txt

COPY . /app

RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. intent_service.proto

EXPOSE 8000

CMD ["python", "run.py"]
