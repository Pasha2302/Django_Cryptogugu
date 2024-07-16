from app.models import BaseCoin, Airdrops, Coin


class BaseContextManager:
    def __init__(self):
        self.base_coins = BaseCoin.objects.all()
        self.count_coins = Coin.objects.count()
        self.count_airdrops = Airdrops.objects.count()

    def get_context (self):
        return {
            'top_rate_items': {
                'base_coins_list': self.base_coins,
                'count_coins_int': self.count_coins,
                'count_airdrops_int': self.count_airdrops,
            }
        }

