# Generated by Django 4.2.13 on 2024-07-11 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact_us', '0002_contactus_responded'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactus',
            name='respond',
            field=models.BooleanField(choices=[(False, 'NO'), (True, 'YES')], default=False),
        ),
    ]
