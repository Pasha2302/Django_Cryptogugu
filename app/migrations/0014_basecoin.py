# Generated by Django 5.0.6 on 2024-07-16 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_alter_coin_contract_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseCoin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('symbol', models.CharField(max_length=50)),
                ('contract_address', models.CharField(blank=True, max_length=52, null=True)),
                ('pair_url', models.URLField()),
                ('market_cap', models.DecimalField(blank=True, decimal_places=2, max_digits=35, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=34, max_digits=64, null=True)),
                ('volume_usd', models.DecimalField(decimal_places=2, max_digits=20)),
                ('volume_btc', models.DecimalField(decimal_places=2, max_digits=20)),
                ('price_change_24h', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price Change 24h')),
                ('path_coin_img', models.CharField(max_length=255)),
                ('path_chain_img', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date Added')),
            ],
            options={
                'verbose_name': 'Base Coin',
                'verbose_name_plural': 'Base Coins',
                'ordering': ['id'],
            },
        ),
    ]