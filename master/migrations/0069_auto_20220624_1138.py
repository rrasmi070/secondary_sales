# Generated by Django 3.2.9 on 2022-06-24 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0068_auto_20220623_2303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='archived_salesdata',
            name='status_3rd_party',
        ),
        migrations.RemoveField(
            model_name='salesdata',
            name='status_3rd_party',
        ),
    ]
