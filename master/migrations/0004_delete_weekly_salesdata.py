# Generated by Django 3.2.9 on 2022-01-14 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0003_remove_salesdata_ale_date_time111'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Weekly_SalesData',
        ),
    ]
