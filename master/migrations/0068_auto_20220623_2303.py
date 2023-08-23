# Generated by Django 3.2.9 on 2022-06-23 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0067_invalid_log_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='archived_salesdata',
            name='status_3rd_party',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='salesdata',
            name='status_3rd_party',
            field=models.BooleanField(default=False),
        ),
    ]
