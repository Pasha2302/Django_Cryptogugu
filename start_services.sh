#!/bin/bash

# Создание директории для логов, если она не существует
mkdir -p Celery_Logs

# Запустите Celery worker в фоновом режиме и запишите логи
nohup celery -A src worker -l info > Celery_Logs/celery_worker.log 2>&1 &

# Запустите Celery Beat в фоновом режиме и запишите логи
nohup celery -A src beat -l info > Celery_Logs/celery_beat.log 2>&1 &

echo "All services have been started and are running in the background."
