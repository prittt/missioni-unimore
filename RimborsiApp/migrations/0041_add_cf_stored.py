# Generated by Django 2.2.3 on 2020-01-22 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RimborsiApp', '0040_add_profile_phone_enddate'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='cf',
            field=models.CharField(default='', max_length=16),
        ),
    ]
