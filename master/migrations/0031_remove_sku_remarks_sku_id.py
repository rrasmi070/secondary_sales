# Generated by Django 3.2.9 on 2022-01-19 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0030_auto_20220119_1343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sku_remarks',
            name='sku_id',
        ),
    ]
