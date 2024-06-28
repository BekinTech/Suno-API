FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt --no-cache-dir

COPY . .

ENV PORT 8080

CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT}
