# Base image
FROM python:3.11.7-slim

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY [  \
    "requirements/main.txt", \
    "requirements/dev.txt", \
    "./alembic.ini", \
    "./static", \
    "./pyproject.toml", \
    "./run.sh", \
    "./" \
    ]
RUN apt-get update && \
    apt-get install -y libgomp1 curl gnupg && \
    curl -fsSL https://ollama.com/install.sh | sh && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r main.txt -r dev.txt

# # Configure NVIDIA Container Toolkit (if GPU ver.)
# RUN curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
#     && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
#     sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
#     tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
# RUN apt-get update && \
#     apt-get install -y nvidia-container-toolkit && \
#     nvidia-ctk runtime configure --runtime=docker

# copy project
COPY ./src ./src

# Make run.sh executable
RUN chmod +x ./run.sh

# Set entrypoint
ENTRYPOINT bash ./run.sh