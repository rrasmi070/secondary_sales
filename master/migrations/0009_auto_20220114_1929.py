# Generated by Django 3.2.9 on 2022-01-14 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0008_rename_updated_on_salesdata_last_updated_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salesdata',
            old_name='created_on',
            new_name='created_date',
        ),
        migrations.RenameField(
            model_name='salesdata',
            old_name='updated_by',
            new_name='last_updated',
        ),
    ]
