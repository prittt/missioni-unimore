# Generated by Django 2.2.2 on 2019-06-25 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RimborsiApp', '0011_add_categorie_stati'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='missione',
            name='targa',
        ),
        migrations.AddField(
            model_name='missione',
            name='scontrino',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]
