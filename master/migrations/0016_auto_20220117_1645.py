# Generated by Django 3.2.9 on 2022-01-17 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0015_alter_salesdata_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesdata',
            name='tranisition_source',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='salesdata',
            name='tranisition_type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
