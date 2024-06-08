# import os
# import logging
# import multiprocessing
# Файл конфигурации Gunicorn


# Количество воркеров (процессов), которые будут обрабатывать запросы.
workers = 4

# Хост и порт, на котором Gunicorn будет слушать входящие соединения.
bind = "127.0.0.1:8000"

# Путь к файлу, в котором будет храниться PID процесса Gunicorn.
pidfile = f"gunicorn_pid.txt"

# Это указывает Gunicorn на путь к вашему проекту Django.
pythonpath = '/home/pavelpc/PycharmProjects/Working_Projects/Django_Cryptogugu/'

# Путь к статическим файлам Django (CSS, JavaScript, изображения и т.д.).
# Должен соответствовать настройке STATIC_ROOT в файле настроек Django.
raw_env = "DJANGO_STATIC_PATH=/home/pavelpc/PycharmProjects/Working_Projects/Django_Cryptogugu/cryptogugu/static"

# Путь к файлу, в который будет записываться лог ошибок Gunicorn.
# errorlog = "logServerCasino_gunicorn.log"

# Настройки воркеров, Дополнительные параметры для оптимизации производительности.
max_requests = 1000
timeout = 30
keepalive = 2
max_requests_jitter = 50
# workers = multiprocessing.cpu_count() * 2 + 1

# Настройка логирования:
loglevel = 'debug' # Увеличить уровень логирования:
errorlog = './gunicorn-error.log'
accesslog = './gunicorn-access.log'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'


# Запуск асинхронного Uvicorn:
# gunicorn my_app.asgi:application -k uvicorn.workers.UvicornWorker -c gunicorn_config.py

# Запуск не асинхронного Gunicorn:
# gunicorn my_app.wsgi:application -c gunicorn_config.py
