# Generated by Django 2.2.2 on 2019-06-20 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RimborsiApp', '0008_add_automobile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='automobile',
            options={'verbose_name_plural': 'Automobili'},
        ),
        migrations.AddField(
            model_name='missione',
            name='automobile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='RimborsiApp.Automobile'),
        ),
    ]