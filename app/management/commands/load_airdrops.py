import json
from datetime import datetime
from django.core.management.base import BaseCommand
from app.models import Airdrops


class Command(BaseCommand):
    help = 'Load airdrops from JSON file into the database'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']

        with open(json_file, 'r') as file:
            data = json.load(file)

        for item in data:
            # Преобразование статуса из строки в булево значение
            status = item['status'].lower() == 'active'

            # Преобразование end_date из строки в дату
            end_date = None
            if item['end_date']:
                try:
                    end_date = datetime.strptime(item['end_date'], '%Y-%m-%d').date()
                except ValueError:
                    self.stderr.write(self.style.ERROR(f"Invalid date format for end_date: {item['end_date']}"))

            # Создание и сохранение экземпляра Airdrops
            airdrop = Airdrops(
                name=item['name'],
                path_coin_img=item['path_coin_img'],
                status=status,
                end_date=end_date,
                reward=item['reward']
            )
            airdrop.save()
            self.stdout.write(self.style.SUCCESS(f"Airdrop {airdrop.name} saved successfully"))


# /home/pavelpc/PycharmProjects/Working_Projects/Django_Cryptogugu/cryptogugu/app/management/commands/airdrops.json
# python manage.py load_airdrops path/to/your/jsonfile.json
