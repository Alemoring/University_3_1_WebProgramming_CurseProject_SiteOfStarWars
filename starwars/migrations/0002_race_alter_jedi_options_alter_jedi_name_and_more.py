# Generated by Django 5.1.1 on 2024-09-24 04:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('starwars', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Название')),
            ],
        ),
        migrations.AlterModelOptions(
            name='jedi',
            options={'verbose_name': 'Джедай', 'verbose_name_plural': 'Джедаи'},
        ),
        migrations.AlterField(
            model_name='jedi',
            name='name',
            field=models.TextField(verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='jedi',
            name='padavan',
            field=models.TextField(verbose_name='Падаван'),
        ),
        migrations.AddField(
            model_name='jedi',
            name='race',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='starwars.race'),
        ),
    ]
