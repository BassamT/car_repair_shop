# Dockerfile
FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y gettext && \
    rm -rf /var/lib/apt/lists/*

ENV LANG ar_AR.UTF-8
ENV LANGUAGE ar_AR:ar
ENV LC_ALL ar_AR.UTF-8

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
