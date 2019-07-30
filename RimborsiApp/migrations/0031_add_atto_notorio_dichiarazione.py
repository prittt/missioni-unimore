# Generated by Django 2.2.3 on 2019-07-29 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RimborsiApp', '0030_edit_comuni_in_profile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comune',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='domicilio_fiscale',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='domicilio_fiscale_provincia',
        ),
        migrations.AddField(
            model_name='modulimissione',
            name='atto_notorio_dichiarazione',
            field=models.TextField(blank=True, null=True),
        ),
    ]