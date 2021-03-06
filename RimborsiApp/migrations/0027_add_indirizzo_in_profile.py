# Generated by Django 2.2.3 on 2019-07-16 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RimborsiApp', '0026_add_indirizzo'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='domicilio',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='domicilio', to='RimborsiApp.Indirizzo'),
        ),
        migrations.AddField(
            model_name='profile',
            name='residenza',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='residenza', to='RimborsiApp.Indirizzo'),
        ),
    ]
