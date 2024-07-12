from django.contrib import admin

from app.models import Coin, PromotedCoins


@admin.register(PromotedCoins)
class PromotedCoinsAdmin(admin.ModelAdmin):
    list_display = ('coin', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('coin__name', 'coin__symbol')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('coin')


@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'tags', 'chain', 'market_cap', 'normalized_price', 'created_at', )
    list_display_links = ('name', 'symbol',)

    fields = (
        'name', 'symbol', 'tags', 'chain', 'market_cap', 'price', 'volume_usd', 'volume_btc',
        'price_change_24h', 'votes', 'votes24h', 'market_cap_presale', 'path_coin_img',
        'path_chain_img', 'launch_date_str', 'launch_date',
    )

    def normalized_price(self, obj):
        return obj.normalized_price

    normalized_price.short_description = 'Coin Price'