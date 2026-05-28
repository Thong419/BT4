FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN python -m pip install --no-cache-dir --timeout 120 --retries 10 -r /app/requirements.txt

COPY . /app

EXPOSE 8501

CMD ["streamlit", "run", "interface.py", "--server.address=0.0.0.0", "--server.port=8501"]
