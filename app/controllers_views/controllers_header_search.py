import json
from django.db.models import QuerySet
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.http import HttpRequest
from app.models import Coin, Airdrops


class HeaderSearchManager:
    def __init__(self, request: HttpRequest):
        self.__customer_data: dict = json.loads(request.body).get('data')
        self.__context = self.search()
        print(f"\nHeader Search Manager [data]: {self.__customer_data}")

    def search(self):
        if self.__customer_data.get('query'):
            query = self.__customer_data['query']

            # Search in Coin model
            coin_search_vector = SearchVector('name', 'symbol', 'contract_address')
            coin_search_query = SearchQuery(query)
            coin_results = Coin.objects.annotate(
                search=coin_search_vector,
                rank=SearchRank(coin_search_vector, coin_search_query)
            ).filter(search=coin_search_query).order_by('-rank')

            # Search in Airdrops model
            airdrop_results = Airdrops.objects.filter(name__icontains=query)

            print("Coin Results:", coin_results)
            print("Airdrop Results:", airdrop_results)

            return coin_results, airdrop_results

        else:
            return [], []

    def get_context(self):
        coin_results, airdrop_results = self.__context

        coins = [
            {
                'name': coin.name,
                'symbol': coin.symbol,
                'contract_address': coin.contract_address,
                'chain': coin.chain,
                'img_path': f'app/{coin.path_coin_img}'
            } for coin in coin_results
        ]

        airdrops = [
            {
                'name': airdrop.name,
                'status': airdrop.status,
                'end_date': airdrop.end_date,
                'reward': airdrop.reward,
                'img_path': f'app/{airdrop.path_coin_img}'
            } for airdrop in airdrop_results
        ]

        return {
            'coins': coins,
            'airdrops': airdrops,
            'count_coins': len(coins),
            'count_airdrops': len(airdrops)
        }
