FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt ./
RUN apt-get update && apt-get install -y \
    build-essential \
    && pip install -r requirements.txt

COPY . .

ENV PORT 8080

CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT}
