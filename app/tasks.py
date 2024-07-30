# app/celery_tasks.py
from celery import shared_task

from api_coins_data.manager import start_update_coins_data
from app.models import Coin
import numpy as np
from random import randint
import time


# Миграций и запуск Celery
# Миграции для django-celery-beat:
# Эта команда применяется для создания необходимых таблиц в базе данных,
# которые используются для хранения информации о периодических задачах:
#   >> python manage.py migrate django_celery_beat

# Запустите Celery worker и Celery Beat:
#   >> celery -A src worker -l info
#   >> celery -A src beat -l info


@shared_task
def reset_votes24h():
    Coin.objects.update(votes24h=0)


@shared_task
def auto_voting():
    # Выбираем 150 случайных монет, которые еще не были выбраны
    coins = Coin.objects.filter(selected_auto_voting=False).order_by('?')[:150]

    # Задаем параметры нормального распределения
    mean_votes = 20  # Среднее количество голосов
    std_deviation = 6  # Стандартное отклонение

    if coins:
        coin_ids = list(coins.values_list('id', flat=True))
        # Обновляем флаг selected для выбранных монет
        Coin.objects.filter(id__in=coin_ids).update(selected_auto_voting=True)

        for hour in range(10):
            for coin in coins:
                # Генерация случайного количества голосов на основе нормального распределения
                votes = int(np.random.normal(mean_votes, std_deviation))
                # Ограничение голосов от 0 до 20
                # votes = max(0, min(votes, 20))
                votes24h = votes // randint(2, 4)

                coin.votes += votes
                coin.votes24h += votes24h
                coin.save()

            time.sleep(20)  # 1550

    else:
        Coin.objects.update(selected_auto_voting=False)
        print("Все монеты прошли голосование ...")


@shared_task
def start_update_coins():
    start_update_coins_data()

