# Generated by Django 3.2.9 on 2023-02-27 18:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0030_weeklysales_update_log'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='weeklysales_update_log',
            table='weekly_update_log',
        ),
    ]
