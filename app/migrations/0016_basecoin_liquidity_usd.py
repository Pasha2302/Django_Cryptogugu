# Generated by Django 5.0.6 on 2024-07-16 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_coin_liquidity_usd'),
    ]

    operations = [
        migrations.AddField(
            model_name='basecoin',
            name='liquidity_usd',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
    ]
