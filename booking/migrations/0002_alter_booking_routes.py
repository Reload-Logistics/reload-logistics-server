# Generated by Django 4.2.13 on 2024-05-18 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='routes',
            field=models.JSONField(default={'routes': [{'id': 1, 'title': 'eric'}]}),
        ),
    ]
