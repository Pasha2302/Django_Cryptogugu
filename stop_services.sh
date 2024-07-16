#!/bin/bash

# Остановите Celery worker
pkill -f 'celery -A src worker'

# Остановите Celery Beat
pkill -f 'celery -A src beat'

echo "All Celery processes have been stopped."
