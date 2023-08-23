# Generated by Django 3.2.9 on 2022-04-29 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0055_rename_other_hawker_total_total_sku_sales_other_m_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='Repeat_count',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wd_id', models.CharField(blank=True, max_length=50, null=True)),
                ('sku_id', models.CharField(blank=True, max_length=50, null=True)),
                ('town_id', models.CharField(blank=True, max_length=50, null=True)),
                ('sale_date_time', models.DateField(blank=True, max_length=50, null=True)),
                ('transaction_source', models.CharField(blank=True, max_length=50, null=True)),
                ('repeat_time', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
    ]
