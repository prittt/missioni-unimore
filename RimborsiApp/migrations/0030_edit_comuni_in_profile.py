# Generated by Django 2.2.3 on 2019-07-26 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RimborsiApp', '0029_edit_luogonascita'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indirizzo',
            name='comune',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='comuni_italiani.Comune'),
        ),
        migrations.AlterField(
            model_name='indirizzo',
            name='provincia',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='comuni_italiani.Provincia'),
        ),
    ]
