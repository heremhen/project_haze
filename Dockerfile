# Base image
FROM python:3.11.7-slim

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ["requirements/main.txt", "requirements/dev.txt", "./"]
RUN apt-get update && \
    apt-get install -y libgomp1 && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r main.txt -r dev.txt

# copy project
COPY . .

# Make run.sh executable
RUN chmod +x ./run.sh

# Set entrypoint
ENTRYPOINT bash ./run.sh