import uuid
from itertools import chain
from django.core.paginator import Paginator
from django.http import HttpRequest

from app.data_coins import get_data_coins
from app.models import UserSettings


class IndexContextManager:
    def __init__(self, request: HttpRequest, current_page=None):
        self.__user_id_str = request.COOKIES.get('userId')
        self.current_uri = request.build_absolute_uri()
        self.base_url = self.__get_base_url()
        self.__data_coins = get_data_coins(count_data=1000)
        self.__per_page = abs(self.__get_per_page())
        self.__paginator = Paginator(self.__data_coins, self.__per_page)

        if current_page is not None: self.__page_number = current_page
        else: self.__page_number = self.__get_page_number(request)

        if self.__page_number > self.__paginator.num_pages:
            self.__page_number = self.__paginator.num_pages
            self.current_uri = self.base_url + f"/?page={self.__page_number}"

        self.nex_page = self.base_url + f"/?page={self.__page_number + 1}"
        self.prev_page = self.__get_prev_page()

        self.__context = {
            'menu_items': [
                {'name': 'Coin Ranking', 'url': 'index'},
                {'name': 'Airdrops', 'url': 'airdrops'},
                {'name': 'Promotion', 'url': '#'},
                {'name': 'Games', 'url': '#'},
                {'name': 'Free Signals', 'url': '#'},
                {'name': 'About Us', 'url': '#'},
            ],

            'select_number_lines': [10, 20, 50, 100, ],

            'rows_number': self.__per_page,
            'page_obj': self.__get_page_obj(),
            'paginator': self.__paginator,
            'page_number': self.__page_number,
            'pagination': self.__calculate_pagination(),
            'page_title': self.__get_page_title(),

            'nex_page': self.nex_page,
            'prev_page': self.prev_page,
            'current_uri': self.current_uri if self.__page_number > 1 else self.base_url,
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

    def __get_per_page(self):
        per_page = 10
        if self.__user_id_str is not None:
            try:
                user_id = uuid.UUID(self.__user_id_str)
                user_settings = UserSettings.objects.get(user_id=user_id)
                per_page = user_settings.per_page
            except UserSettings.DoesNotExist:
                print('\nПользователь Не Найден в Базе!')
        return per_page

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
