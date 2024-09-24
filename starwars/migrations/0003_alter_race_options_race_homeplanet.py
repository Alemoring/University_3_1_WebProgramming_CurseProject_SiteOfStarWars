# Generated by Django 5.1.1 on 2024-09-24 04:23

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('starwars', '0002_race_alter_jedi_options_alter_jedi_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='race',
            options={'verbose_name': 'Расса', 'verbose_name_plural': 'Рассы'},
        ),
        migrations.AddField(
            model_name='race',
            name='homePlanet',
            field=models.TextField(default=django.utils.timezone.now, verbose_name='Родная планета'),
            preserve_default=False,
        ),
    ]
