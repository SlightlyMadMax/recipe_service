FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

RUN mkdir /app
WORKDIR /app

RUN mkdir -p /app/logs

COPY ./src/requirements.txt /app/
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY ./src /app/
COPY ./.env /app/.env
COPY ./.env.db /app/.env.db
COPY ./docker-entrypoint.sh /app/docker-entrypoint.sh
COPY ./wait-postgres.sh /app/wait-postgres.sh

RUN chmod +x docker-entrypoint.sh
