import json
from itertools import chain
from django.core.paginator import Paginator
from django.http import HttpRequest

from app.controllers_views.controllers_settings_user import SettingsManager
from app.models import Coin
from django.utils import timezone
from datetime import timedelta
from django.utils.translation import gettext as _
from decimal import Decimal


class FilterCoin:
    def __init__(self, settings: SettingsManager):
        self.__data_coins = Coin.objects.all()

        if settings.user_settings_obj:
            if settings.user_settings_obj.all_time_best:
                self.__data_coins = Coin.objects.order_by('-votes')

            elif settings.user_settings_obj.today_hot:
                self.__data_coins = Coin.objects.order_by('-votes24h')

            if settings.user_settings_obj.presale:
                self.__data_coins = self.__data_coins.filter(market_cap_presale=True)

            if settings.user_settings_obj.audited:
                self.__data_coins = self.__data_coins.filter(tags__contains=["Audited"])

            if settings.user_settings_obj.doxxed:
                self.__data_coins = self.__data_coins.filter(tags__contains=["Doxxed"])

            if settings.user_settings_obj.new:
                twelve_hours_ago = timezone.now() - timedelta(hours=12)
                self.__data_coins = self.__data_coins.filter(created_at__gte=twelve_hours_ago)

            if settings.user_settings_obj.item_sub_symbol and settings.user_settings_obj.item_sub_symbol != 'None':
                self.__data_coins = self.__data_coins.filter(chain=settings.user_settings_obj.item_sub_symbol.upper())

            if settings.user_settings_obj.head_filter:
                symbol, sort = settings.user_settings_obj.head_filter.split(',')
                if symbol != 'None':
                    self.__head_filter_coins(symbol, sort)
            # self.print_time_since_creation()


    def __head_filter_coins(self, symbol: str, sort: str):
        print(f"\n__head_filter_coins: {symbol=}  /  {sort=}")
        if sort == "DESC": self.__data_coins = self.__data_coins.order_by(f'-{symbol}')
        else: self.__data_coins = self.__data_coins.order_by(symbol)

        if symbol == 'market_cap':
            original_coins = list(self.__data_coins)
            coins_market_cap = [coin for coin in original_coins if coin.market_cap is not None]
            coins_market_cap_none = [coin for coin in original_coins if coin.market_cap is None and not coin.market_cap_presale]
            coins_market_cap_presale = [coin for coin in original_coins if coin.market_cap_presale]
            self.__data_coins = coins_market_cap + coins_market_cap_presale + coins_market_cap_none

        elif symbol == 'price':
            original_coins = list(self.__data_coins)
            coins_price = [coin for coin in original_coins if coin.price is not None]
            coins_price_none = [coin for coin in original_coins if coin.price is None ]
            self.__data_coins = coins_price + coins_price_none

    def get_coins(self):
        return self.__data_coins

    def print_time_since_creation(self):
        for coin in self.__data_coins:
            time_since_creation = timezone.now() - coin.created_at
            print(f"\n\n{coin.name} was created {time_since_creation} ago")



class IndexContextManager:
    def __init__(self, request: HttpRequest):
        self.settings = SettingsManager(request)
        self.customer_data = self.settings.customer_data

        self.current_uri = request.build_absolute_uri()
        self.base_url = self.__get_base_url()

        self.__data_coins = FilterCoin(self.settings).get_coins()
        self.__per_page = self.settings.per_page
        self.__paginator = Paginator(self.__data_coins, self.__per_page)

        if self.customer_data.get('currentPage') is not None: self.__page_number = self.customer_data['currentPage']
        elif self.customer_data.get('morePage') is not None: self.__page_number = self.customer_data['morePage']
        else: self.__page_number = self.__get_page_number(request)

        if self.__page_number > self.__paginator.num_pages:
            self.__page_number = self.__paginator.num_pages
            self.current_uri = self.base_url + f"/?page={self.__page_number}"

        self.nex_page = self.base_url + f"/?page={self.__page_number + 1}"
        self.prev_page = self.__get_prev_page()

        self.__page_obj = self.__get_page_obj()
        self.__context = {
            'menu_items': [
                {'name': _('Coin Ranking'), 'url': 'index'},
                {'name': _('Airdrops'), 'url': 'airdrops'},
                {'name': _('Promotion'), 'url': '#'},
                {'name': _('Games'), 'url': '#'},
                {'name': _('Free Signals'), 'url': '#'},
                {'name': _('About Us'), 'url': '#'},
            ],

            'select_number_lines': [10, 20, 50, 100, ],

            'rows_number': self.__per_page,
            'page_obj': self.__page_obj,
            'paginator': self.__paginator,
            'page_start_index': (self.__page_obj.number - 1) * self.__page_obj.paginator.per_page,

            'page_number': self.__page_number,
            'pagination': self.__calculate_pagination(),
            'page_title': self.__get_page_title(),

            'nex_page': self.nex_page,
            'prev_page': self.prev_page,
            'current_uri': self.current_uri if self.__page_number > 1 else self.base_url,

            'filter_item': self.settings.get_filter_item(),
        }

    def get_context(self) -> dict:
        return self.__context

    def __get_base_url(self):
        uri = self.current_uri.split('/?')[0]
        if uri.endswith('/'): uri = uri.rstrip('/')
        return uri

    @staticmethod
    def __get_page_number(request):
        page_number = 1
        if request.GET.get('page'):
            page_number = abs(int(request.GET.get('page')))
        if request.POST.get('page'):
            page_number = abs(int(request.POST.get('page')))
        return page_number

    def __get_prev_page(self):
        return self.base_url + f"/?page={self.__page_number - 1}" if self.__page_number > 2 else self.base_url

    def __get_page_obj(self):
        print("\nPaginator All Pages: ", self.__paginator.num_pages)
        print("Current Page number: ", self.__page_number)
        return self.__paginator.get_page(self.__page_number)

    def __get_page_title(self):
        if self.__page_number == 1:
            page_title = "And New Cryptocurrency Listing Portal | CryptoGugu"
        else:
            page_title = f"New Cryptocurrency And DeFi Listing Portal - Page {self.__page_number} | CryptoGugu"
        return page_title

    def __calculate_pagination(self):
        pagination = [1]
        current_page = self.__page_number
        total_pages = self.__paginator.num_pages

        if total_pages < 15: return [p for p in range(1, total_pages + 1)]

        if current_page > 2:
            pagination.extend(
                [p for p in range(current_page -2, current_page + 3)
                 if 1 < p < total_pages]
            )
        else:
            pagination.extend([p for p in range(current_page, current_page + 3) if p not in [1, total_pages]])

        pagination.append(total_pages)

        average_from_start = ['...', round((pagination[0] + pagination[1]) / 2), '...']
        average_from_end = ['...', round((pagination[-1] + pagination[-2]) / 2), '...']
        if 5 < current_page < (total_pages - 5):
            pagination.insert(1, average_from_start)
            pagination.insert(-1, average_from_end)
            pagination = list(chain.from_iterable(x if isinstance(x, list) else [x] for x in pagination))

        if '...' not in pagination:
            if (pagination[-1] - pagination[-2]) > 4:
                pagination.insert(-1, average_from_end)
                pagination = list(chain.from_iterable(x if isinstance(x, list) else [x] for x in pagination))
            elif total_pages - current_page <= 5:
                pagination.insert(1, average_from_start)
                pagination = list(chain.from_iterable(x if isinstance(x, list) else [x] for x in pagination))

        return pagination
