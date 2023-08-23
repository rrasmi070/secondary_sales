# Generated by Django 3.2.9 on 2022-02-07 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0033_transition_history_tranisition_source'),
    ]

    operations = [
        migrations.CreateModel(
            name='Archived_SalesData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_category', models.CharField(blank=True, max_length=20, null=True)),
                ('sku_id', models.CharField(blank=True, max_length=100, null=True)),
                ('wd_id', models.CharField(blank=True, max_length=100, null=True)),
                ('town_id', models.CharField(blank=True, max_length=100, null=True)),
                ('sales_date_time', models.DateField(blank=True, null=True)),
                ('local_sales_retail', models.FloatField(blank=True, default=0, null=True)),
                ('local_sales_dealer', models.FloatField(blank=True, default=0, null=True)),
                ('local_sales_modern_trade', models.FloatField(blank=True, default=0, null=True)),
                ('local_sales_hawker', models.FloatField(blank=True, default=0, null=True)),
                ('total_local_sales', models.FloatField(blank=True, default=0, null=True)),
                ('outstation_sales_reatil', models.FloatField(blank=True, default=0, null=True)),
                ('outstation_sales_dealer', models.FloatField(blank=True, default=0, null=True)),
                ('outstation_sales_modern_trade', models.FloatField(blank=True, default=0, null=True)),
                ('outstation_sales_hawker', models.FloatField(blank=True, default=0, null=True)),
                ('total_outstation_sales', models.FloatField(blank=True, default=0, null=True)),
                ('other_sales_reatil', models.FloatField(blank=True, default=0, null=True)),
                ('other_sales_dealer', models.FloatField(blank=True, default=0, null=True)),
                ('other_sales_modern_trade', models.FloatField(blank=True, default=0, null=True)),
                ('total_other_sales', models.FloatField(blank=True, default=0, null=True)),
                ('other_issues_damage', models.FloatField(blank=True, default=0, null=True)),
                ('other_issues_return', models.FloatField(blank=True, default=0, null=True)),
                ('other_issues_other', models.FloatField(blank=True, default=0, null=True)),
                ('total_issue', models.FloatField(blank=True, default=0, null=True)),
                ('grand_total', models.FloatField(blank=True, default=0, null=True)),
                ('created_by', models.CharField(blank=True, max_length=100, null=True)),
                ('last_updated', models.CharField(blank=True, max_length=100, null=True)),
                ('tranisition_source', models.CharField(blank=True, max_length=50, null=True)),
                ('created_date', models.DateTimeField(blank=True, null=True)),
                ('last_updated_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.BooleanField(default=True)),
                ('freez_status', models.BooleanField(default=False)),
                ('weekly_sales', models.CharField(blank=True, max_length=50, null=True)),
                ('tranisition_type', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 'transaction_archived_salesdata',
            },
        ),
    ]
