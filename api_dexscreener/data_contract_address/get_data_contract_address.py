import os
import re
import asyncio
import time
from asyncio import AbstractEventLoop

from UseDB.async_mysql_database import AsyncMySQLManager
from cryptogugu.api_dexscreener.Tools import toolbox
import django
from get_contract_address_from_site import get_contract

# Установка переменной окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')
# Инициализация Django
django.setup()

from app.models import Coin


def count_duplicates(coins: list[dict]):
    return len(coins) - len(set(map(lambda x: x['symbol'], coins)))


def get_only_unique_coins(coins: list[dict]):
    new_data = []
    check_coins_symbol = []

    for coin in coins:
        if coin['symbol'] not in check_coins_symbol:
            check_coins_symbol.append(coin['symbol'])
            new_data.append(coin)

    print(f"\nCount New Data: {len(new_data)}")
    return new_data


def extract_bsc_contract_address(contract_info):
    if " " not in contract_info:
        return contract_info

    bsc_address = None
    parts = contract_info.split()
    for i, part in enumerate(parts):
        if part == 'BSC' and i + 1 < len(parts):
            bsc_address = parts[i + 1]
            break
    return bsc_address


def is_valid_bsc_address(address):
    """
    Проверяет, является ли адрес корректным адресом контракта в сети BSC.
    """
    pattern = re.compile(r'^0x[a-fA-F0-9]{40}$')
    return bool(pattern.match(address))


def get_contract_address_from_JSON():
    count_coins = 0
    coins_db = Coin.objects.all()
    coins_json = toolbox.download_json_data(path_file="FINAL_DATA.json")
    print(f"Count duplicates: {count_duplicates(coins_json)}")
    coins_json = get_only_unique_coins(coins_json)
    print(f"Count duplicates: {count_duplicates(coins_json)}")

    for coin_db in coins_db:
        search = False
        for coin_json in coins_json:
            if coin_db.symbol == coin_json['symbol'] and coin_db.name == coin_json['name']:
                count_coins += 1

                # Получение адреса контракта из JSON данных
                contract_info = coin_json['page_data'].get('binance_smart_chain')
                bsc_address = extract_bsc_contract_address(contract_info)

                try:
                    if bsc_address and is_valid_bsc_address(bsc_address):
                        coin_db.contract_address = bsc_address
                        coin_db.save()
                        search = True
                        break
                except Exception as err:
                    print('binance_smart_chain:', bsc_address)
                    raise err

        if not search:
            coin_db.contract_address = None
            coin_db.save()


    print(f"Count Coins JSON: {count_coins}")


def check_contract_address(get_coins=False):
    count = 0
    coins_without_address = Coin.objects.filter(contract_address__isnull=True)
    # coins_without_address = Coin.objects.filter(contract_address__isnull=False)

    if get_coins: return coins_without_address

    for coin in coins_without_address:
        # coin_dict = coin.__dict__
        count += 1
        print(f"\nМонета без contract_address [{count}]:")
        print(f"Name: {coin.name}\nSymbol: {coin.symbol}\nContract Address: {coin.contract_address}\n")
        get_contract_address_from_api(coin.symbol)
        time.sleep(4)
        # for key, value in coin_dict.items():
        #     print(f"{key}: {value}")
        print("\n" + "==" * 60)


async def search_coin_mydb(name, symbol, db_coin_local):
    query = f"SELECT * FROM coin WHERE name='{name}' AND symbol='{symbol}'"
    result = await db_coin_local.execute_query(query=query, fetch=True)
    total_rows = len(result)
    # print(f"Записей найдено: {total_rows=}")
    for data in result:
        if total_rows > 1:
            for k, v in data.items():
                print(f"{k}:  {v}")
            print('--' * 40)

    print('==' * 40)



def get_contract_address_from_mydb():
    use_db_local = "coinmooner"
    path_config = '/home/pavelpc/PycharmProjects/Working_Projects/Django_Cryptogugu/UseDB/db_config/db_config_local.json'
    db_config_mooner_local = toolbox.download_json_data(path_file=path_config)
    print(db_config_mooner_local)

    db_coin_local = AsyncMySQLManager(db_config_mooner_local, use_db=use_db_local)
    with toolbox.create_loop() as loop:
        loop.run_until_complete(db_coin_local.connect())
        loop: AbstractEventLoop
        try:
            check_coins = check_contract_address(get_coins=True)
            for coin in check_coins:
                # print(f"Name: {coin.name}\nSymbol: {coin.symbol}\nContract Address: {coin.contract_address}\n")
                loop.run_until_complete( search_coin_mydb(coin.name, coin.symbol, db_coin_local) )
        finally:
            # loop.run_until_complete(db_coinmooner.disconnect())
            loop.run_until_complete(db_coin_local.disconnect())
            time.sleep(0.35)


def get_contract_address_from_api(search_coin: str):
    asyncio.run(get_contract(search=search_coin))


def main():
    # get_contract_address_from_JSON()
    # check_contract_address()
    get_contract_address_from_mydb()


if __name__ == '__main__':
    main()
