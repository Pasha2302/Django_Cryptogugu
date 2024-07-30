from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
import uuid
from decimal import Decimal

from django.db.models import QuerySet
from django.core.exceptions import ValidationError


class DefaultManager(models.Manager):
    pass


class SiteSettings(models.Model):
    count_coins = models.IntegerField(null=True, blank=True)
    count_airdrops = models.IntegerField(null=True, blank=True)

    objects: QuerySet = DefaultManager()  # Явное определение менеджера

    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            raise ValidationError('Можно создать только одну запись Site Settings')
        return super(SiteSettings, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return "Site Data"


class ReclamBanner(models.Model):
    POSITION_CHOICES = [
        ('right-banner', 'Top Right Banner'),
        ('left-banner', 'Top Left Banner'),
        ('banner_1', 'Banner Bottom 1'),
        ('banner_2', 'Banner Bottom 2'),
        ('banner_3', 'Banner Bottom 3'),
        ('banner_4', 'Banner Bottom 4'),
        ('banner_5', 'Banner Bottom 5'),
        ('banner_6', 'Banner Bottom 6'),
    ]

    position = models.CharField(max_length=20, choices=POSITION_CHOICES)
    image = models.ImageField(upload_to='banners/')
    link = models.URLField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)  # Для отображения/скрытия баннера

    def is_currently_active(self):
        now = timezone.now()
        return self.is_active and self.start_time <= now <= self.end_time

    class Meta:
        verbose_name = 'Reclam Banner'
        verbose_name_plural = 'Reclam Banners'

    def __str__(self):
        return f"{self.position} banner"


def format_decimal_number(number):
    # print(f"\nNumber: {number} / {type(number)=}")
    number_str = format(number, 'f').rstrip('0')  # Преобразовать число в строку и удалить замыкающие нули
    # print(number_str)
    # if not number_str: return None

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
    theme_site = models.CharField(max_length=10, default='dark')

    today_hot = models.BooleanField(default=False)
    all_time_best = models.BooleanField(default=True)
    gem_pad = models.BooleanField(default=False)
    new = models.BooleanField(default=False)
    presale = models.BooleanField(default=False)
    doxxed = models.BooleanField(default=False)
    audited = models.BooleanField(default=False)

    item_sub_symbol = models.CharField(max_length=20, null=True)

    head_filter = models.CharField(max_length=30, null=True)

    coins_votes = ArrayField(models.CharField(max_length=50), verbose_name="Coins Votes", blank=True, default=list)

    objects = UserSettingsManager()

    def __str__(self):
        return f"Settings for user {self.user_id}"

    def has_voted_for(self, coin_id):
        return coin_id in self.coins_votes

    def vote_for_coin(self, coin_id):
        if not self.has_voted_for(coin_id):
            self.coins_votes.append(coin_id)
            self.save()
            return True
        return False


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


class PromotedCoins(models.Model):
    coin = models.OneToOneField("Coin", on_delete=models.CASCADE, related_name='promoted')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()

    def __str__(self):
        return f"Promoted: {self.coin.name} from {self.start_date} to {self.end_date}"


class Coin(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=50)
    contract_address = models.CharField(max_length=52, blank=True, null=True)
    selected_auto_voting = models.BooleanField(default=False)

    tags = ArrayField(models.CharField(max_length=50), verbose_name="Tags", blank=True, default=list)
    chain = models.CharField(max_length=30)

    market_cap = models.DecimalField(max_digits=35, decimal_places=2, blank=True, null=True)
    price = models.DecimalField(max_digits=64, decimal_places=34, blank=True, null=True)
    liquidity_usd = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

    volume_usd = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    volume_btc = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    price_change_24h = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price Change 24h")

    votes = models.IntegerField(default=0)
    votes24h = models.IntegerField(default=0)
    market_cap_presale = models.BooleanField(default=False)

    path_coin_img = models.ImageField(upload_to='coin_images/', max_length=255)
    path_chain_img = models.ImageField(upload_to='chain_images/', max_length=255)

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


# ==================================================================================================================== #
class BaseCoin(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=50)
    contract_address = models.CharField(max_length=52, blank=True, null=True)
    pair_url = models.URLField(max_length=200)
    market_cap = models.DecimalField(max_digits=35, decimal_places=2, blank=True, null=True)
    price = models.DecimalField(max_digits=64, decimal_places=34, blank=True, null=True)
    liquidity_usd = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

    volume_usd = models.DecimalField(max_digits=20, decimal_places=2)
    volume_btc = models.DecimalField(max_digits=20, decimal_places=2)
    price_change_24h = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price Change 24h")

    path_coin_img = models.CharField(max_length=255)
    path_chain_img = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date Added")

    objects: QuerySet = DefaultManager()  # Явное определение менеджера

    @property
    def normalized_price(self):
        self.price: Decimal
        if self.price is not None:
            return self.price.normalize()
        return None

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["id"]
        verbose_name = "Base Coin"
        verbose_name_plural = "Base Coins"