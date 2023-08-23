# Generated by Django 3.2.9 on 2022-09-09 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_access_log'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='access_log',
            name='sales_save_data',
        ),
        migrations.AddField(
            model_name='access_log',
            name='count',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='access_log',
            name='created_by',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='access_log',
            name='sales_save_date',
            field=models.DateField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='access_log',
            name='updated_by',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='access_log',
            name='updated_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
