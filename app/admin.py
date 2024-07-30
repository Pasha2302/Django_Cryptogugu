from django.contrib import admin

from app.models import Coin, PromotedCoins, BaseCoin, SiteSettings, ReclamBanner
from django import forms
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.html import mark_safe


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Разрешить добавление записи только если её еще нет
        if SiteSettings.objects.exists():
            return False
        return super(SiteSettingsAdmin, self).has_add_permission(request)


@admin.register(ReclamBanner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('position', 'start_time', 'end_time', 'is_active', 'is_currently_active')
    list_filter = ('position', 'is_active', 'start_time', 'end_time')
    search_fields = ('position',)


class PromotedCoinsForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if (start_date and not end_date) or (end_date and not start_date):
            raise forms.ValidationError("Both start date and end date are required if one is filled.")

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date cannot be earlier than start date.")


@admin.register(PromotedCoins)
class PromotedCoinsAdmin(admin.ModelAdmin):
    form = PromotedCoinsForm
    list_display = ('coin', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('coin__name', 'coin__symbol')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('coin')


class CoinAdminForm(forms.ModelForm):
    remove_coin_img = forms.BooleanField(required=False, initial=False)
    remove_chain_img = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = Coin
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CoinAdminForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.path_coin_img:
                self.fields['path_coin_img'].widget = AdminFileWidget()
                self.fields['path_coin_img'].help_text = mark_safe(
                    f'<img src="{self.instance.path_coin_img.url}" style="max-width: 200px; max-height: 200px;" />')
            if self.instance.path_chain_img:
                self.fields['path_chain_img'].widget = AdminFileWidget()
                self.fields['path_chain_img'].help_text = mark_safe(
                    f'<img src="{self.instance.path_chain_img.url}" style="max-width: 200px; max-height: 200px;" />')

    def save(self, commit=True):
        instance = super(CoinAdminForm, self).save(commit=False)
        if self.cleaned_data.get('remove_coin_img') and instance.path_coin_img:
            instance.path_coin_img.delete()
            instance.path_coin_img = None
        if self.cleaned_data.get('remove_chain_img') and instance.path_chain_img:
            instance.path_chain_img.delete()
            instance.path_chain_img = None
        if commit:
            instance.save()
        return instance


@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    form = CoinAdminForm
    list_display = ('display_coin_image', 'name', 'symbol', 'chain', 'normalized_price')
    list_display_links = ('name', 'symbol',)

    def display_coin_image(self, obj):
        if obj.path_coin_img:
            return mark_safe(f'<img src="{obj.path_coin_img.url}" style="width: 50px; height: 50px;" />')
        return "No Image"
    display_coin_image.short_description = 'Coin Image'

    def display_chain_image(self, obj):
        if obj.path_chain_img:
            return mark_safe(f'<img src="{obj.path_chain_img.url}" style="width: 50px; height: 50px;" />')
        return "No Image"
    display_chain_image.short_description = 'Chain Image'

    def normalized_price(self, obj):
        return obj.normalized_price

    normalized_price.short_description = 'Coin Price'


@admin.register(BaseCoin)
class BaseCoinAdmin(admin.ModelAdmin):
    pass
