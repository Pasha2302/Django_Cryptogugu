# Generated by Django 5.0.6 on 2024-06-28 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_usersettings_head_filter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coin',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=34, max_digits=64, null=True),
        ),
    ]
