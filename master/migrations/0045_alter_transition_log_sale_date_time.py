# Generated by Django 3.2.9 on 2022-02-18 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0044_transition_log_sale_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transition_log',
            name='sale_date_time',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
