#!/bin/bash

# Function to check the exit status of a command and exit the script if it fails
check_status() {
    if [ $? -ne 0 ]; then
        echo "Error: $1 failed"
        exit 1
    fi
}

# Start Celery worker
celery -A src.celery.app worker -l info --concurrency=2 &
check_status "Starting Celery worker"

# Start Celery Flower for monitoring
celery -A src.celery.app flower -l info &
check_status "Starting Celery Flower"

# Start Celery Beat for periodic tasks
celery -A src.celery.app beat -l INFO &
check_status "Starting Celery Beat"

# # Run Alembic migrations
# alembic revision --autogenerate &
# check_status "Running Alembic revision"
# alembic upgrade head &
# check_status "Running Alembic upgrade"

# Start the FastAPI server with Uvicorn
uvicorn src.main:app --host 0.0.0.0 --workers 2
check_status "Starting Uvicorn server"
