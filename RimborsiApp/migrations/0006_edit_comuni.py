# Generated by Django 2.2.2 on 2019-06-14 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RimborsiApp', '0005_add_missione'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comune',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Comuni',
            },
        ),
        migrations.AlterModelOptions(
            name='missione',
            options={'verbose_name_plural': 'Missioni'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name_plural': 'Profili'},
        ),
    ]