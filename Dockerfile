FROM python:3.12.2-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

VOLUME /root/.cache/pip

RUN apt-get update && apt-get install -y \
    gcc \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements/main.txt .
COPY requirements/dev.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r main.txt -r dev.txt

COPY . .

RUN chmod +x ./run.sh && \
    addgroup --gid 1001 --system hazel && \
    adduser --no-create-home --shell /bin/false --disabled-password --uid 1001 --system --group hazel && \
    chown hazel:hazel ./static && \
    chown hazel:hazel db.sqlite3

ENTRYPOINT ["./run.sh"]
USER hazel