import json
import uuid

from django.http import HttpRequest

from app.models import UserSettings


def clear_data():
    UserSettings.objects.all().delete()


def save_user(user=None):
    user_id = uuid.uuid4() if user is None else user
    data_id, created = UserSettings.objects.get_or_create(user_id=user_id)
    data = {'user_id': str(data_id.user_id)}
    print(f"\n{data_id=}\n{created=}")
    return data


class SettingsManager:
    def __init__(self, request: HttpRequest):
        self.user_id_str = request.COOKIES.get('userId')
        self.user_settings_obj = None
        self.customer_data = dict()

        if self.user_id_str is not None and self.user_id_str != 'null':
            print(f"{self.user_id_str=}")
            self.user_id = uuid.UUID(self.user_id_str)
            self.user_settings_obj = UserSettings.objects.get(user_id=self.user_id)

        if request.method == 'POST':
            self.customer_data = json.loads(request.body).get('data')
            print(f"\n\nCustomer Data: {self.customer_data}")
            self.__save_settings()

        self.per_page = abs(self.__get_per_page())


    def get_filter_item(self):
        if self.user_settings_obj is not None:
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
                # ['BSC', 'SOL', 'ETH', 'MATIC', 'TRON', 'BASE', 'TON', 'CRONOS', 'HARMONY', 'ETHEREUMFAIR', 'PULSECHAIN', 'ARBITRUM']
                'item_sub': [
                    {'active': False, 'title': 'Ethereum', 'symbol': 'eth'},
                    {'active': False, 'title': 'WAX', 'symbol': 'wax'},
                    {'active': False, 'title': 'SOLANA', 'symbol': 'sol'},
                    {'active': False, 'title': 'Binance Smart Chain', 'symbol': 'bsc'},
                    {'active': False, 'title': 'Tron', 'symbol': 'tron'},
                ],
                'chain_button_title': 'Chain',

            }

            for item_sub in filter_item['item_sub']:
                if item_sub['symbol'] == str(self.user_settings_obj.item_sub_symbol):
                    item_sub['active'] = True
                    filter_item['chain_button_title'] = f"Chain: {item_sub['title']}"
        else:
            filter_item = {
                'item': [
                    {'data_info': 'today_hot', 'active': False, 'title': 'Today`s Hot'},
                    {'data_info': 'all_time_best', 'active': True, 'title': 'All Time Best'},

                    {'data_info': 'gem_pad', 'active': False, 'title': 'GemPad'},
                    {'data_info': 'new', 'active': False, 'title': 'New'},
                    {'data_info': 'presale', 'active': False, 'title': 'Presale'},
                    {'data_info': 'doxxed', 'active': False, 'title': 'Doxxed'},
                    {'data_info': 'audited', 'active': False, 'title': 'Audited'},
                ],
                'item_sub': [
                    {'active': False, 'title': 'Ethereum', 'symbol': 'eth'},
                    {'active': False, 'title': 'WAX', 'symbol': 'wax'},
                    {'active': False, 'title': 'SOLANA', 'symbol': 'sol'},
                    {'active': False, 'title': 'Binance Smart Chain', 'symbol': 'bsc'},
                    {'active': False, 'title': 'Tron', 'symbol': 'tron'},
                ],
                'chain_button_title': 'Chain',

            }
        return filter_item


    def __get_per_page(self):
        per_page = 10
        if self.user_settings_obj is not None:
            try:
                per_page = self.user_settings_obj.per_page
            except UserSettings.DoesNotExist:
                print('\nПользователь Не Найден в Базе!')
        return int(per_page)


    def __save_settings(self):
        per_page = self.customer_data['per_page']
        filter_item_list = self.customer_data.get('filter_item')
        if self.user_settings_obj is not None:
            try:
                self.user_settings_obj.per_page = per_page
                if filter_item_list:
                    for filter_item in filter_item_list:
                        data_info = filter_item['data_info']
                        if hasattr(self.user_settings_obj, data_info):  # Проверяем, что атрибут существует
                            setattr(self.user_settings_obj, data_info, filter_item['active'])
                        else:
                            print(f"[method = 'POST'] Атрибут '{data_info}' не найден в модели UserSettings!")

                self.user_settings_obj.save()
                print(f"\nUser Settings Obj: {vars(self.user_settings_obj)}")
            except UserSettings.DoesNotExist as err:
                print(err)
                print("[method = 'POST'] Пользователь не найден в базе!")
