# Generated by Django 3.2.9 on 2022-01-17 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0024_alter_salesdata_sales_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesdata',
            name='sales_date_time',
            field=models.DateField(blank=True, null=True),
        ),
    ]
