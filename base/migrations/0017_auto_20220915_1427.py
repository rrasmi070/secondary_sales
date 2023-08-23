# Generated by Django 3.2.9 on 2022-09-15 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_auto_20220909_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_reset_password',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='reset_password_date',
            field=models.DateField(blank=True, default=False, null=True),
        ),
    ]
