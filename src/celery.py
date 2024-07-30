# src/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

app = Celery('app_cryptogugu')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# Добавляем конфигурации Celery
# app.conf.update(
    # Включить события задач для мониторинга
    # task_send_sent_event=True,

    # # Устанавливаем брокера сообщений (в данном случае Redis)
    # broker_url='redis://localhost:6379/0',
    #
    # # Устанавливаем URL для хранения результатов выполнения задач (в данном случае Redis)
    # result_backend='redis://localhost:6379/0',

    # Устанавливаем уровень логирования
    # worker_log_format='[%(asctime)s: %(levelname)s/%(processName)s] %(message)s',
    # worker_task_log_format='[%(asctime)s: %(levelname)s/%(processName)s] Task %(task_name)s[%(task_id)s]: %(message)s',

    # # Время ожидания перед завершением задачи (в секундах)
    # task_soft_time_limit=300,  # 5 минут
    #
    # # Время ожидания завершения задачи (в секундах)
    # task_time_limit=600,  # 10 минут
    #
    # # Количество задач, которые каждый воркер может выполнить перед перезапуском
    # worker_max_tasks_per_child=100,
    #
    # # Частота вывода состояния (в секундах)
    # worker_send_task_events=True,
    #
    # # Настройка пулла воркеров (использование "prefork" или "solo")
    # worker_concurrency=8,
    #
    # # Настройки повторных попыток задач
    # task_acks_late=True,  # Подтверждение задачи только после завершения
    # task_reject_on_worker_lost=True,  # Повторить задачу, если воркер потерян
    #
    # # Кэширование результатов задач
    # result_cache_max=5000,  # Максимальное количество кэшированных результатов
# )
