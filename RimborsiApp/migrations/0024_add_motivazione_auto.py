# Generated by Django 2.2.2 on 2019-07-10 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RimborsiApp', '0023_add_dottorando_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='missione',
            name='mezzi_previsti',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='missione',
            name='motivazione_automobile',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]