# Use a base image with Python
FROM --platform=linux/arm64 python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VENV_PATH=/opt/venv

# Create a virtual environment
RUN python3 -m venv $VENV_PATH

ENV PATH="$VENV_PATH/bin:$PATH"

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY pure/ .
COPY entrypoint.sh/ .

EXPOSE 8000
