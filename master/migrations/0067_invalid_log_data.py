# Generated by Django 3.2.9 on 2022-05-16 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0066_salesdata_distrcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invalid_log_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distrcode', models.CharField(blank=True, max_length=30, null=True)),
                ('dist_id', models.CharField(blank=True, max_length=30, null=True)),
                ('dist_type', models.CharField(blank=True, max_length=30, null=True)),
                ('sale_date', models.CharField(blank=True, max_length=30, null=True)),
                ('region', models.CharField(blank=True, max_length=30, null=True)),
                ('town_code', models.CharField(blank=True, max_length=30, null=True)),
                ('prodcode', models.CharField(blank=True, max_length=30, null=True)),
                ('state', models.CharField(blank=True, max_length=30, null=True)),
                ('duration_start', models.CharField(blank=True, max_length=30, null=True)),
                ('plan_type', models.CharField(blank=True, max_length=30, null=True)),
                ('franchisecode', models.CharField(blank=True, max_length=30, null=True)),
                ('brandcode', models.CharField(blank=True, max_length=30, null=True)),
                ('catcode', models.CharField(blank=True, max_length=30, null=True)),
                ('local_retail', models.CharField(blank=True, max_length=30, null=True)),
                ('local_dealer', models.CharField(blank=True, max_length=30, null=True)),
                ('local_MT', models.CharField(blank=True, max_length=30, null=True)),
                ('local_HA', models.CharField(blank=True, max_length=30, null=True)),
                ('out_retail', models.CharField(blank=True, max_length=30, null=True)),
                ('out_dealer', models.CharField(blank=True, max_length=30, null=True)),
                ('out_MT', models.CharField(blank=True, max_length=30, null=True)),
                ('out_HA', models.CharField(blank=True, max_length=30, null=True)),
                ('other_retail', models.CharField(blank=True, max_length=30, null=True)),
                ('other_dealer', models.CharField(blank=True, max_length=30, null=True)),
                ('other_MT', models.CharField(blank=True, max_length=30, null=True)),
                ('other_issued_damage', models.CharField(blank=True, max_length=30, null=True)),
                ('other_issued_returns', models.CharField(blank=True, max_length=30, null=True)),
                ('transaction_source', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
    ]
