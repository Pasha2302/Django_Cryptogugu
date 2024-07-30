from __future__ import annotations

import asyncio
import os

import aiohttp
import django
from asgiref.sync import sync_to_async

from .Tools import toolbox
from .module_aiorequest import RequestAiohttp

# Установка переменной окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')
# Инициализация Django
django.setup()

from app.models import Coin, BaseCoin
from django.db.models.query import QuerySet

headers = {'accept': 'application/json, text/plain, */*', }


class DexscreenerAPIManager:
    def __init__(self, coins_data: QuerySet, api_url: str | None):
        self.__coins_data: list[Coin,] = list(coins_data)
        self.__api_url = api_url
        self.__session = None
        self.__dexscreener_api_data_coins = []
        self.no_data_coins = []

        self.__check_dict_quote_token_and_rialto = {
            'solana': ('SOL', 'raydium'),
            'ethereum': ('WETH', 'uniswap'),
            'bsc': ('WBNB', 'pancakeswap'),
            'base': ('WETH', 'uniswap'),
            'polygon': ('WMATIC', 'uniswap'),
        }

    def start(self, limit: int | None = 10, base_coins=None):
        print("\nSTART")
        asyncio.run(self.__get_data_coin(limit, base_coins))
        print(f"\n END")

    async def __get_data_coin(self, limit, base_coins):
        async with toolbox.AiohttpSession(limit=5, total=600).create_session() as session:
            session: aiohttp.ClientSession
            self.__session = session

            if base_coins is None:
                list_requests_coroutine = self.__get_list_requests(self.__coins_data, limit)
                print(f'\n\nВсего монет по API Dexscreener: {len(list_requests_coroutine)}')
                for cor in list_requests_coroutine:
                    result = await cor['request']
                    self.__check_coin(api_data=result, input_coin=cor['input_coin'])

            else:
                for base_coins_obj in self.__coins_data:
                    base_coins_obj: BaseCoin
                    data_api = await self.__request(input_coin=base_coins_obj.pair_url)
                    if data_api.get('pair'):
                        data_api = data_api['pair']
                        base_coins_obj.price = data_api['priceUsd']
                        base_coins_obj.volume_usd = data_api['volume']['h24']
                        base_coins_obj.liquidity_usd = data_api['liquidity']['usd']
                        base_coins_obj.market_cap = data_api['fdv']
                        await sync_to_async(base_coins_obj.save)()

    def __get_list_requests(self, coins, limit):
        list_requests = []
        for coin in coins:
            input_coin = {
                'coin_id': coin.id, 'name': coin.name, 'symbol': coin.symbol,
                'contract_address': coin.contract_address, 'chain': self.__rename_chain(coin.chain),
                # 'name': coin['name'], 'symbol': coin['symbol'], 'contract_address': coin['contract_address'],
            }
            list_requests.append(
                {'request': self.__request(input_coin), 'input_coin': input_coin}
            )
            if limit is not None:
                limit -= 1
                if limit == 0: break
        return list_requests

    def __check_coin(self, api_data, input_coin):
        if not api_data.get('pairs'): return

        datas = [
            data_search for data_search in api_data['pairs']
            if data_search and data_search['baseToken']['address'] == input_coin['contract_address']
        ]

        if datas:
            datas_api_sort = sorted(
                datas,
                key=lambda pair_data: pair_data["liquidity"]["usd"] if pair_data.get('liquidity') else 0,
                reverse=True
            )
            data = {
                'search_coin': input_coin, 'data_api': self.__check_chain(input_coin, datas_api_sort)
            }

            if data.get('data_api'):
                self.__dexscreener_api_data_coins.append(data)

    def save_data_db(self):
        for api_data in self.__dexscreener_api_data_coins:
            coin_id = api_data['search_coin']['coin_id']
            coin_obj = Coin.objects.get(id=coin_id)

            coin_obj.price = api_data['data_api']['priceUsd']
            coin_obj.volume_usd = api_data['data_api']['volume']['h24']
            coin_obj.liquidity_usd = api_data['data_api']['liquidity']['usd']
            coin_obj.market_cap = api_data['data_api']['fdv']
            coin_obj.save()

    def __check_chain(self, data_search_coin, datas_api):
        verified_data_quote_token = []
        verified_data_rialto = []
        for d_api in datas_api:
            if data_search_coin['chain'].lower() == d_api['chainId'].lower():
                if self.__check_quote_token_symbol(d_api, d_api['chainId']):
                    verified_data_quote_token.append(d_api)

        for i_api in verified_data_quote_token:
            if self.__check_rialto(i_api, i_api['chainId']):
                verified_data_rialto.append(i_api)

        if verified_data_rialto:
            return verified_data_rialto[0]
        elif verified_data_quote_token:
            return verified_data_quote_token[0]

    def __check_quote_token_symbol(self, data_api: dict, input_chain: str) -> bool:
        quote_token_symbol_check = self.__check_dict_quote_token_and_rialto.get(input_chain)
        if quote_token_symbol_check:
            return quote_token_symbol_check[0] == data_api['quoteToken']['symbol']

    def __check_rialto(self, data_api: dict, input_chain: str) -> bool:  # проверка по бирже.
        check_rialto = self.__check_dict_quote_token_and_rialto.get(input_chain)
        if check_rialto:
            return check_rialto[1] == data_api['dexId']

    @staticmethod
    def __rename_chain(chain_coin):
        chain: str = chain_coin
        if chain.lower() == 'eth':
            chain = 'ethereum'
        elif chain.lower() == 'sol':
            chain = 'solana'
        elif chain.lower() == 'matic':
            chain = 'polygon'
        return chain

    async def __request(self, input_coin):
        if self.__api_url is not None:
            url = self.__api_url.format(input_coin['contract_address'])
        else:
            url = input_coin
        async_request = RequestAiohttp(
            session=self.__session, method='get', url=url, headers=headers, cookies=None,
            # proxy='https://141.94.17.33:22222',
        )
        data_server = await async_request.get_data_server()
        if isinstance(data_server, dict):
            if not data_server.get('pairs'):
                print(f"\n\n[DexscreenerAPIManager] No Data Coin:\nData Server: {data_server}\nInput Data: {input_coin}")
                self.no_data_coins.append(input_coin)
            return data_server
        else:
            print(f"\nNo __request DATA: !:\n{input_coin=}")


def get_coins_to_json():
    import json
    from django.core.serializers import serialize

    new_data = []
    # Получение всех записей модели Coin
    coins = Coin.objects.all()
    # Сериализация данных в JSON формат
    coins_json = json.loads(serialize('json', coins))

    for coin in coins_json:
        coin_fields = coin['fields']
        # Преобразование поля tags из строки в список, если оно не пустое
        if 'tags' in coin_fields and isinstance(coin_fields['tags'], str):
            try:
                coin_fields['tags'] = json.loads(coin_fields['tags'])
            except json.JSONDecodeError:
                coin_fields['tags'] = []
        new_data.append(coin_fields)

    with open('coins_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(new_data, json_file, ensure_ascii=False, indent=4)



class MobulaAPIManager:
    def __init__(self, data_coins: list[dict,]):
        self.__data_coins = data_coins
        self.__datas_api = []
        self.__no_data_coins_modula = []
        self.__headers = {
            'accept': 'application/json, text/plain, */*',
            'Authorization': 'c19c0edb-0430-4930-a650-1244a4304b49'
        }
        print(f'\nВсего монет по API Modula: {len(data_coins)}')

    def start(self):
        print("\nSTART")
        asyncio.run(self.__get_data_coin())
        print(f"\n END")


    async def __get_data_coin(self):
        async with toolbox.AiohttpSession(limit=5, total=600).create_session() as session:
            session: aiohttp.ClientSession

            tasks_list = [self.__request(session=session, input_coin=data) for data in self.__data_coins]
            # results = await asyncio.gather(*tasks_list, return_exceptions=True)
            # for res in results:
            for task in tasks_list:
                res = await task
                if not res.get('no_data'):
                    self.__datas_api.append(res)
                else:
                    print(f'\n[MobulaAPIManager] Bed Request!:\n{res}')
                    self.__no_data_coins_modula.append(res)

    async def __request(self, session, input_coin):
        contract_address = input_coin['contract_address']
        chain = self.__rename_chain(input_coin['chain'])
        url = f'https://api.mobula.io/api/1/market/data?asset={contract_address}&blockchain={chain}'

        async_request = RequestAiohttp(
            session=session, method='get', url=url, headers=self.__headers, cookies=None,
            # proxy='https://141.94.17.33:22222',
        )
        data_coin_api = await async_request.get_data_server()

        if isinstance(data_coin_api, dict):
            if not data_coin_api.get('data'):
                return {'no_data': {'input_coin': input_coin, 'data_coin_api': data_coin_api}}
            return {'input_coin': input_coin, 'data_coin_api': data_coin_api['data']}
        else:
            raise TypeError(f"\nNo __request DATA: !:\n{input_coin=}\n{data_coin_api=}")

    def save_data_coins_to_json(self):
        if self.__datas_api:
            toolbox.save_json_data(json_data=self.__datas_api, path_file='api_mobula_data_coins.json')
            toolbox.save_json_data(json_data=self.__no_data_coins_modula, path_file='api_mobula_no_data_coins.json')
        else: print('\nMobulaAPIManager [save_data_coins_to_json]: Нет Данных для сохранения в JSON ...')

    def save_data_coins_to_db(self):
        if self.__datas_api:
            for api_data in self.__datas_api:
                coin_id = api_data['input_coin']['coin_id']
                coin_obj = Coin.objects.get(id=coin_id)

                coin_obj.price = api_data['data_coin_api']['price']
                coin_obj.volume_usd = api_data['data_coin_api'].get('volume', 0.0)
                coin_obj.liquidity_usd = api_data['data_coin_api']['liquidity']
                coin_obj.market_cap = api_data['data_coin_api']['market_cap']
                coin_obj.save()

        else: print('\nMobulaAPIManager [save_data_coins_to_db]: Нет Данных для сохранения в BD ...')

    @staticmethod
    def __rename_chain(chain_coin: str):
        chain = chain_coin.lower()
        if chain == 'bsc':
            chain = 'BNB Smart Chain (BEP20)'
        return chain


def start_update_coins_data():
    api_url_dexscreener = 'https://api.dexscreener.com/latest/dex/tokens/{}'

    coins_objects = Coin.objects.all()
    dexscreener_api = DexscreenerAPIManager(coins_data=coins_objects, api_url=api_url_dexscreener)
    dexscreener_api.start(limit=None)
    dexscreener_api.save_data_db()

    coins_objects = BaseCoin.objects.all()
    dexscreener_api_base_coin = DexscreenerAPIManager(coins_data=coins_objects, api_url=None)
    dexscreener_api_base_coin.start(limit=None, base_coins=True)

    if dexscreener_api.no_data_coins:
        modula_api = MobulaAPIManager(data_coins=dexscreener_api.no_data_coins)
        modula_api.start()
        modula_api.save_data_coins_to_db()
        modula_api.save_data_coins_to_json()


if __name__ == '__main__':
    pass
    # Coin.objects.all().delete()
    # Coin.objects.update(volume_btc=0)
    # start_update_coins_data()
