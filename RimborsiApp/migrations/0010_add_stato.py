# Generated by Django 2.2.2 on 2019-06-21 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RimborsiApp', '0009_edit_automobile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Stati',
            },
        ),
        migrations.RenameField(
            model_name='missione',
            old_name='destinazione',
            new_name='citta_destinazione',
        ),
        migrations.AddField(
            model_name='missione',
            name='stato_destinazione',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='RimborsiApp.Stato'),
        ),
    ]
