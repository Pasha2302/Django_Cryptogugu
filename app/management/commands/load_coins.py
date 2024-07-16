import json
from datetime import datetime
from django.core.management.base import BaseCommand
from app.models import Coin


class Command(BaseCommand):
    help = 'Load coins from JSON file into the database'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']

        with open(json_file, 'r') as file:
            data = json.load(file)

        for item in data:
            # Преобразование launch_date из строки в дату
            launch_date = None
            if item['launch_date']:
                try:
                    launch_date = datetime.strptime(item['launch_date'], '%d/%m/%Y').date()
                except ValueError:
                    self.stderr.write(self.style.ERROR(f"Invalid date format for launch_date: {item['launch_date']}"))

            # Создание и сохранение экземпляра Coin
            market_cap_presale = item['market_cap_presale'] if item['market_cap_presale'] else False
            coin = Coin(
                name=item['name'],
                symbol=item['label'],
                tags=item.get('tags', []),
                chain=item['chain'],
                market_cap=item.get('market_cap', None),
                price=item['price'],
                volume_usd=item['volume_usd'],
                volume_btc=item['volume_btc'],
                price_change_24h=item['price_change_24h'],
                votes=item['votes'],
                votes24h=item['votes24h'],
                path_coin_img=item['path_coin_img'],
                path_chain_img=item['path_chain_img'],
                launch_date=launch_date,
                market_cap_presale=market_cap_presale,
                launch_date_str=item.get('launch_date_str', None)
            )
            coin.save()
            self.stdout.write(self.style.SUCCESS(f"Coin {coin.name} saved successfully"))


# /home/pavelpc/PycharmProjects/Working_Projects/Django_Cryptogugu/cryptogugu/app/management/commands/coins_data.json
# python manage.py load_coins path/to/your/jsonfile.json
