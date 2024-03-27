# Base image
FROM python:3.11.7-slim

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

VOLUME /root/.cache/pip

# install dependencies
COPY requirements/main.txt requirements/main.txt
COPY requirements/dev.txt requirements/dev.txt
COPY [  \
    "./alembic.ini", \
    "./static", \
    "./pyproject.toml", \
    "./run.sh", \
    "./" \
    ]
RUN apt-get update && \
    apt-get install -y libgomp1 && \
    # curl gnupg g++ gdb make ninja-build rsync zip && \
    # curl -fsSL https://ollama.com/install.sh | sh && \
    pip install --upgrade pip && \
    pip install --cache-dir=/root/.cache/pip -r requirements/main.txt -r requirements/dev.txt

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