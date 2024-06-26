from django.contrib.postgres.fields import ArrayField
from django.db import models
import uuid
from decimal import Decimal

from django.db.models import QuerySet


class UserSettingsManager(models.Manager):
    pass


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

    objects: QuerySet = UserSettingsManager()

    def __str__(self):
        return f"Settings for user {self.user_id}"


class Coin(models.Model):
    name = models.CharField(max_length=255)
    label = models.CharField(max_length=50)
    tags = ArrayField(models.CharField(max_length=50), verbose_name="Tags", blank=True, default=list)
    chain = models.CharField(max_length=30)

    market_cap = models.DecimalField(max_digits=35, decimal_places=2, blank=True, null=True)
    price = models.DecimalField(max_digits=64, decimal_places=34)

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

    objects: QuerySet = UserSettingsManager()  # Явное определение менеджера

    @property
    def normalized_price(self):
        self.price: Decimal
        normalize_price = self.price.normalize()
        # if normalize_price == 0: normalize_price = '—'
        return normalize_price

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["id"]
        verbose_name = "Coin"
        verbose_name_plural = "Coins"

