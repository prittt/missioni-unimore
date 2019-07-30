# Generated by Django 2.2.2 on 2019-07-04 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RimborsiApp', '0022_remove_name_cognome_in_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='anno_dottorato',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='scuola_dottorato',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='tutor',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]