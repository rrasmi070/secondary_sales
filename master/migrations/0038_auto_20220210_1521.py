# Generated by Django 3.2.9 on 2022-02-10 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0037_transition_log_tranisition_source'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sku_remarks',
            old_name='brand_category',
            new_name='tranisition_type',
        ),
        migrations.RemoveField(
            model_name='sku_remarks',
            name='town_id',
        ),
    ]
