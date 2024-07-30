import json
import uuid

from django.http import HttpRequest

from app.models import UserSettings


def clear_data():
    UserSettings.objects.all().delete()


def save_user(user=None):
    user_id = uuid.uuid4() if user is None else user
    user_settings_obj = UserSettings.objects.get_or_create_default_settings(user_id)
    data = {'user_id': str(user_settings_obj.user_id)}
    print(f"\n{data=}")
    return data


class SettingsManager:
    def __init__(self, request: HttpRequest):
        self.user_id_str = request.COOKIES.get('userId')
        self.user_settings_obj = None
        self.customer_data = dict()
        self.status_votes = dict()

        if self.user_id_str is not None and self.user_id_str != 'null':
            self.user_id = uuid.UUID(self.user_id_str)
            self.user_settings_obj, _ = UserSettings.objects.get_or_create(user_id=self.user_id)
        else:
            self.user_settings_obj = UserSettings.objects.get_or_create_default_settings(user_id=None)

        if request.method == 'POST':
            self.customer_data = json.loads(request.body).get('data')
            print(f"\n\nCustomer Data: {self.customer_data}")

            if self.customer_data.get('vole_coin_id'):
                self.status_votes = self.__save_vote_coin_id()
            elif self.customer_data.get('theme_site'):
                self.set_theme_site()
            else:
                self.__save_settings_filter()

        self.per_page = abs(self.__get_per_page())

    def set_theme_site(self):
        self.user_settings_obj.theme_site = self.customer_data['theme_site']
        self.user_settings_obj.save()

    def get_filter_item(self):
        filter_item = {
            'item': [
                {'data_info': 'today_hot', 'active': self.user_settings_obj.today_hot, 'title': 'Today`s Hot'},
                {'data_info': 'all_time_best', 'active': self.user_settings_obj.all_time_best, 'title': 'All Time Best'},

                {'data_info': 'gem_pad', 'active': self.user_settings_obj.gem_pad, 'title': 'GemPad'},
                {'data_info': 'new', 'active': self.user_settings_obj.new, 'title': 'New'},
                {'data_info': 'presale', 'active': self.user_settings_obj.presale, 'title': 'Presale'},
                {'data_info': 'doxxed', 'active': self.user_settings_obj.doxxed, 'title': 'Doxxed'},
                {'data_info': 'audited', 'active': self.user_settings_obj.audited, 'title': 'Audited'},
            ],

            'item_sub': [
                {'active': False, 'title': 'Ethereum', 'symbol': 'eth'},
                {'active': False, 'title': 'WAX', 'symbol': 'wax'},
                {'active': False, 'title': 'SOLANA', 'symbol': 'sol'},
                {'active': False, 'title': 'Binance Smart Chain', 'symbol': 'bsc'},
                {'active': False, 'title': 'Tron', 'symbol': 'tron'},
            ],
            'chain_button_title': 'Chain',

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

        for item_sub in filter_item['item_sub']:
            if item_sub['symbol'] == str(self.user_settings_obj.item_sub_symbol):
                item_sub['active'] = True
                filter_item['chain_button_title'] = f"Chain: {item_sub['title']}"
                break

        data_head_filter = self.user_settings_obj.head_filter
        if data_head_filter:
            args = data_head_filter.split(',')
            for head_filter in filter_item['head_filter']:
                symbol, sort = args[0], args[1]
                if head_filter['symbol'] == symbol:
                    head_filter['active'] = True
                    head_filter['sort'] = sort
                    break

        return filter_item

    def __get_per_page(self):
        per_page = 10
        if self.user_settings_obj is not None:
            try:
                per_page = self.user_settings_obj.per_page
            except UserSettings.DoesNotExist:
                print('\nПользователь Не Найден в Базе!')
        return int(per_page)

    def __save_settings_filter(self):
        per_page = self.customer_data['per_page']
        filter_item_list = self.customer_data.get('filter_item')

        try:
            self.user_settings_obj.per_page = per_page
            if filter_item_list:
                for filter_item in filter_item_list:
                    data_info = filter_item['data_info']
                    if hasattr(self.user_settings_obj, data_info):  # Проверяем, что атрибут существует
                        setattr(self.user_settings_obj, data_info, filter_item['active'])
                    else:
                        print(f"[ __save_settings ] Атрибут '{data_info}' не найден в модели UserSettings!")

            self.user_settings_obj.save()
            print(f"\nUser Settings Obj: {vars(self.user_settings_obj)}")
        except UserSettings.DoesNotExist as err:
            print(err)
            print("[method = 'POST'] Пользователь не найден в базе!")

    def __save_vote_coin_id(self):
        if self.user_settings_obj:
            vole_coin_id = self.customer_data['vole_coin_id']
            if self.user_settings_obj.vote_for_coin(vole_coin_id):
                return {"status": "Vote registered", "vole_coin_id": vole_coin_id}
            else:
                return {"status": "You have already voted for this coin"}
        return {"status": "User settings not found"}
