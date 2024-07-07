from django.contrib.postgres.fields import ArrayField
from django.db import models
import uuid
from decimal import Decimal

from django.db.models import QuerySet


def format_decimal_number(number):
    number_str = format(number, 'f').rstrip('0')  # Преобразовать число в строку и удалить замыкающие нули
    # print(number_str)

    if '.' in number_str:
        integer_part, fractional_part = number_str.split('.')

        if not fractional_part or int(fractional_part) == 0:
            return integer_part if integer_part else "0"

        first_non_zero_idx = len(fractional_part) - len(fractional_part.lstrip('0'))
        zero_count = first_non_zero_idx

        if zero_count > 3:
            significant_part = fractional_part[first_non_zero_idx:]
            formatted_number = f"0.|{zero_count}|{significant_part}"
            return formatted_number
        else:
            return number_str
    else:
        return number_str


class DefaultManager(models.Manager):
    pass


class UserSettingsManager(models.Manager):
    def get_or_create_default_settings(self, user_id):
        # ID дефолтного пользователя
        default_user_id = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
        if user_id is None:
            user_id = default_user_id
        settings, created = self.get_or_create(user_id=user_id)
        return settings


class UserSettings(models.Model):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    per_page = models.PositiveIntegerField(default=10)

    today_hot = models.BooleanField(default=False)
    all_time_best = models.BooleanField(default=True)
    gem_pad = models.BooleanField(default=False)
    new = models.BooleanField(default=False)
    presale = models.BooleanField(default=False)
    doxxed = models.BooleanField(default=False)
    audited = models.BooleanField(default=False)

    item_sub_symbol = models.CharField(max_length=20, null=True)

    head_filter = models.CharField(max_length=30, null=True)

    objects = UserSettingsManager()

    def __str__(self):
        return f"Settings for user {self.user_id}"



class Airdrops(models.Model):
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    end_date = models.DateField(blank=True, null=True)
    reward = models.CharField(max_length=255)
    path_coin_img = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date Added")
    objects: QuerySet = DefaultManager()

    def __str__(self):
        return self.name


class Coin(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=50)
    contract_address = models.CharField(max_length=42, blank=True, null=True)

    tags = ArrayField(models.CharField(max_length=50), verbose_name="Tags", blank=True, default=list)
    chain = models.CharField(max_length=30)

    market_cap = models.DecimalField(max_digits=35, decimal_places=2, blank=True, null=True)
    price = models.DecimalField(max_digits=64, decimal_places=34, blank=True, null=True)

    volume_usd = models.DecimalField(max_digits=20, decimal_places=2)
    volume_btc = models.DecimalField(max_digits=20, decimal_places=2)
    price_change_24h = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price Change 24h")

    votes = models.IntegerField(default=0)
    votes24h = models.IntegerField(default=0)
    market_cap_presale = models.BooleanField(default=False)

    path_coin_img = models.CharField(max_length=255)
    path_chain_img = models.CharField(max_length=255)

    launch_date_str = models.CharField(max_length=50, blank=True, null=True)
    launch_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date Added")

    objects: QuerySet = DefaultManager()  # Явное определение менеджера

    @property
    def normalized_price(self):
        self.price: Decimal
        if self.price is not None:
            normalize_price = self.price.normalize()
            return format_decimal_number(normalize_price)
        return None

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["id"]
        verbose_name = "Coin"
        verbose_name_plural = "Coins"

