#!/bin/bash

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -vz "$POSTGRES_HOST" "$POSTGRES_PORT"; do
      sleep 0.15
    done

    echo "PostgreSQL started"
fi



echo "[MIGRATE]"
python manage.py migrate --no-input

echo "[COLLECT STATIC]"
python manage.py collectstatic --no-input

echo "[RUN SERVER]"
gunicorn culinary.wsgi:application --bind 0.0.0.0:8002