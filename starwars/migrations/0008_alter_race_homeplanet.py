# Generated by Django 5.1.1 on 2024-10-08 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('starwars', '0007_alter_character_fraction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='race',
            name='homePlanet',
            field=models.TextField(verbose_name='Планет'),
        ),
    ]
