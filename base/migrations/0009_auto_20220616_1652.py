# Generated by Django 3.2.9 on 2022-06-16 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_password_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='password_history',
            name='password',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='password_history',
            name='user_type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
