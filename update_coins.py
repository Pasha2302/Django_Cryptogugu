import os
from api_coins_data.manager import start_update_coins_data
from api_coins_data.get_coin_from_api import get_contract_address

from app.models import Coin

# Установка переменной окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')


def rename_path_img():
    obj_coins = Coin.objects.all()

    for coin in obj_coins:
        path_coin_img = coin.path_coin_img.name
        path_chain_img = coin.path_chain_img.name

        new_path_coin_img = os.path.join('coin_images', path_coin_img.split('/')[-1])
        new_path_chain_img = os.path.join('chain_images', path_chain_img.split('/')[-1])

        coin.path_coin_img.name = new_path_coin_img
        coin.path_chain_img.name = new_path_chain_img

        coin.save()


if __name__ == '__main__':
    try:
        rename_path_img()
        # get_contract_address()
        # start_update_coins_data()
    except Exception as err:
        print(f"\nERROR: {err}")
