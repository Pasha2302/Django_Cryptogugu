import os
import asyncio
import aiohttp
from .Tools import toolbox
from .module_aiorequest import RequestAiohttp
import django

# Установка переменной окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')
# Инициализация Django
django.setup()

from app.models import Coin
from django.db.models.query import QuerySet

headers = {
    'accept': 'application/json, text/plain, */*',
    # 'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
}


class SearchCoinAPI:
    def __init__(self, coins_data: QuerySet, api_url: str):
        self.__coins_data: list[Coin,] = list(coins_data)
        self.__api_url = api_url
        self.__session = None

    def start(self, limit=10):
        print("\nSTART")
        r = asyncio.run(self.__search_coin(limit))
        print(f"\n Start: {r}")

    async def __search_coin(self, limit):
        async with toolbox.AiohttpSession(limit=5, total=600).create_session() as session:
            session: aiohttp.ClientSession
            self.__session = session
            list_requests_coroutine = self.__get_list_requests(self.__coins_data, limit)
            print(f'\n\nВсего запросов: {len(list_requests_coroutine)}')
            for cor in list_requests_coroutine:
                result = await cor['request']
                self.__check_coin(api_data=result, data_search_coin=cor['data_search_coin'])

        return "END"

    def __check_coin(self, api_data, data_search_coin):
        print(f"\n{data_search_coin=}")
        print(f"{api_data=}")
        datas = [
            data_search for data_search in api_data.get('pairs')
            if data_search and data_search['baseToken']['name'] == data_search_coin['name']
               and data_search['baseToken']['symbol'] == data_search_coin['symbol']
        ]

        if datas:
            data = {
                'search_coin': data_search_coin, 'data_api': self.__check_chain(data_search_coin, datas)
            }
            print('--' * 60)
            if data.get('data_api'):
                toolbox.save_json_complementing(json_data=data, path_file='new_coins_data.json', ind=True)

    @staticmethod
    def __check_chain(data_search_coin, datas_api):
        for d_api in datas_api:
            if data_search_coin['chain'].lower() == d_api['chainId'].lower():
                return d_api
        return datas_api[0]

    def __get_list_requests(self, coins, limit):
        list_requests = []
        for coin in coins:
            data_search_coin = {
                'coin_id': coin.id, 'name': coin.name, 'symbol': coin.symbol,
                'contract_address': coin.contract_address, 'chain': self.__rename_chain(coin.chain),
                # 'name': coin['name'], 'symbol': coin['symbol'], 'contract_address': coin['contract_address'],
            }
            list_requests.append({'request': self.__request(coin.name), 'data_search_coin': data_search_coin})
            limit -= 1
            if limit == 0: break
        return list_requests

    @staticmethod
    def __rename_chain(chain_coin):
        chain: str = chain_coin
        if chain.lower() == 'eth':
            chain = 'ethereum'
        if chain.lower() == 'sol':
            chain = 'solana'
        if chain.lower() == 'matic':
            chain = 'polygon'
        return chain

    async def __request(self, search_coin_name):
        url = self.__api_url.format(search_coin_name)
        async_request = RequestAiohttp(
            session=self.__session, method='get', url=url, headers=headers, cookies=None,
            # proxy='https://141.94.17.33:22222',
        )
        data_server = await async_request.get_data_server()
        if isinstance(data_server, dict):
            return data_server

    @staticmethod
    def set_contract_and_delete_bad_coins():
        coins_json = toolbox.download_json_data(path_file='new_coins_data.json')

        coins_id = []
        for coin in coins_json:
            if coin['search_coin']['chain'].lower() == coin['data_api']['chainId'].lower():
                coin_id = coin['search_coin']['coin_id']
                coin_obj = Coin.objects.get(id=coin_id)

                coin_obj.contract_address = coin['data_api']['baseToken']['address']
                coin_obj.save()
                coins_id.append(coin_id)

        # Удаление всех монет, кроме тех, которые в списке ids_to_keep
        Coin.objects.exclude(id__in=coins_id).delete()


def get_contract_address():
    api_url_dexscreener_search = 'https://api.dexscreener.com/latest/dex/search/?q={}'
    coins_objects = Coin.objects.all()

    search_coin = SearchCoinAPI(coins_data=coins_objects, api_url=api_url_dexscreener_search)
    search_coin.start(limit=coins_objects.__len__())

    search_coin.set_contract_and_delete_bad_coins()

    # delete_coins = ['Binance coin', 'Ethereum Token', 'Bitcoin', 'Solana']
    #
    # for _delete_c in delete_coins:
    #     coin_obj = Coin.objects.get(name=_delete_c)
    #
    #     print('Name:', coin_obj.name)
    #     print('Symbol:', coin_obj.symbol)
    #     print('Chain:', coin_obj.chain)
    #     coin_obj.delete()
