# Generated by Django 3.2.9 on 2022-02-09 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0036_transition_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='transition_log',
            name='tranisition_source',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
