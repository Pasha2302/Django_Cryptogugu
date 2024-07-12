from __future__ import annotations

import json
from itertools import chain
from django.core.paginator import Paginator
from django.http import HttpRequest

from app.controllers_views.controllers_settings_user import SettingsManager
from app.models import Coin
from django.utils import timezone
from datetime import timedelta
from django.utils.translation import gettext as _


class FilterCoin:
    def __init__(self, settings: SettingsManager | None = None, data_coins=None):
        if data_coins is None:
            self.__data_coins = Coin.objects.all()
        else:
            self.__data_coins = data_coins

        if settings is not None and settings.user_settings_obj:
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
                    self.head_filter_coins(symbol, sort)
            # self.print_time_since_creation()


    def head_filter_coins(self, symbol: str, sort: str):
        # print(f"\n__head_filter_coins: {symbol=}  /  {sort=}")
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

    @staticmethod
    def get_coins_tops_section():
        return {
            'trending': Coin.objects.order_by('-volume_usd')[:5],
            'most_viewed': Coin.objects.order_by('-votes')[:5],
            'top_gainers': Coin.objects.order_by('-price')[:5],
        }

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

        self.__filter_coin_obj = FilterCoin(self.settings)
        self.__data_coins = self.__filter_coin_obj.get_coins()
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
            'coins_tops_section': self.__filter_coin_obj.get_coins_tops_section()
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


class PromotedCoinsTableManager:
    def __init__(self, request: HttpRequest):
        self.__customer_data = json.loads(request.body).get('data')
        self.__data_head_filter = self.__customer_data.get('active')
        self.args = self.__data_head_filter.split(',')

        self.__data_coins = Coin.objects.filter(promoted__isnull=False).select_related('promoted')
        # print(f"\nData Coins Promoted: {self.__data_coins,}")

        filter_coins_obj = FilterCoin(data_coins=self.__data_coins)
        filter_coins_obj.head_filter_coins(symbol=self.args[0], sort=self.args[1])
        self.__context = {
            'filter_item': self.get_filter_item(),
            'page_obj': {'object_list': filter_coins_obj.get_coins()},
            'page_start_index': 0,
        }

    def get_filter_item(self):
        filter_item = {
            'head_filter': [
                {'active': False, 'title': 'Market Cap', 'symbol': 'market_cap', 'sort': 'ASC'},
                {'active': False, 'title': 'Price', 'symbol': 'price', 'sort': 'ASC'},
                {'active': False, 'title': 'Volume', 'symbol': 'volume_usd', 'sort': 'ASC'},
                {'active': False, 'title': '24h', 'symbol': 'price_change_24h', 'sort': 'ASC'},
                {'active': False, 'title': 'Launch Date', 'symbol': 'launch_date', 'sort': 'ASC'},
                {'active': False, 'title': 'Votes', 'symbol': 'votes', 'sort': 'ASC'},
                {'active': False, 'title': 'Votes 24', 'symbol': 'votes24h', 'sort': 'ASC'},
            ],
        }

        if self.args:
            for head_filter in filter_item['head_filter']:
                symbol, sort = self.args[0], self.args[1]
                if head_filter['symbol'] == symbol:
                    head_filter['active'] = True
                    head_filter['sort'] = sort
                    break

        return filter_item

    def get_context(self):
        return self.__context


class VoteManager:
    def __init__(self, request: HttpRequest):
        self.__settings = SettingsManager(request)
        self.__data_vote = None

    def get_data_vote(self):
        return self.__data_vote

    def check_and_save_vote(self):
        if self.__settings.status_votes.get("status") == "Vote registered":
            self.__data_vote = self.save_vote(self.__settings.status_votes['vole_coin_id'])
        else: self.__data_vote = self.__settings.status_votes

    @staticmethod
    def save_vote(vole_coin_id):
        # Увеличьте количество голосов для указанной монеты
        coin = Coin.objects.get(id=vole_coin_id)
        coin.votes += 1
        coin.votes24h += 1
        coin.save()
        return {"daily_vote": coin.votes24h, "vote": coin.votes}



