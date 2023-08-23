# Generated by Django 3.2.9 on 2022-12-15 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0077_delete_apistatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='Apistatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('running_date', models.DateField(blank=True, null=True)),
                ('status', models.BooleanField(default=False)),
                ('api', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
    ]
