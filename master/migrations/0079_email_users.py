# Generated by Django 3.2.9 on 2023-01-04 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0078_apistatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email_users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100)),
                ('use_for', models.CharField(max_length=100)),
                ('email_cc', models.BooleanField(default=True)),
                ('email_to', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
