from app.models import BaseCoin, Airdrops, Coin, SiteSettings


class BaseContextManager:
    def __init__(self):
        self.site_settings: SiteSettings = SiteSettings.objects.first()
        self.base_coins = BaseCoin.objects.all()
        print('\nSite Settings Obj:', self.site_settings)

        if self.site_settings and self.site_settings.count_coins:
            self.count_coins = self.site_settings.count_coins
        else:
            self.count_coins = Coin.objects.count()

        if self.site_settings and self.site_settings.count_airdrops:
            self.count_airdrops = self.site_settings.count_airdrops
        else:
            self.count_airdrops = Airdrops.objects.count()

    def get_context (self):
        return {
            'top_rate_items': {
                'base_coins_list': self.base_coins,
                'count_coins_int': self.count_coins,
                'count_airdrops_int': self.count_airdrops,
            }
        }

