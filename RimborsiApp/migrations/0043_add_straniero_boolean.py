# Generated by Django 2.2.3 on 2020-01-24 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RimborsiApp', '0042_add_data_for_foreign_profiles'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='straniero',
            field=models.BooleanField(default=False),
        ),
    ]
