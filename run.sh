#!/bin/bash

check_status() {
    if [ $? -ne 0 ]; then
        echo "Error: $1 failed"
        exit 1
    fi
}

celery -A src.celery.app worker -l info -c 2 &
# celery -A src.celery.app worker -l info --concurrency=2 -O fair -P prefork --without-gossip --pool=gevent &
check_status "Starting Celery worker"

celery -A src.celery.app flower -l info &
check_status "Starting Celery Flower"

celery -A src.celery.app beat -l INFO &
check_status "Starting Celery Beat"

# alembic revision --autogenerate &
# check_status "Running Alembic revision"
# alembic upgrade head &
# check_status "Running Alembic upgrade"

uvicorn src.main:app --host 0.0.0.0 --workers 2
check_status "Starting Uvicorn server"
