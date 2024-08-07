# Generated by Django 5.0.7 on 2024-07-26 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_basecoin_liquidity_usd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coin',
            name='volume_btc',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='coin',
            name='volume_usd',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
    ]
