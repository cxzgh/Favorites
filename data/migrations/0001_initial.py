# Generated by Django 4.1.7 on 2023-02-26 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmakers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookmaker', models.CharField(max_length=50)),
                ('bookmaker_name', models.CharField(max_length=50)),
                ('cotaP1', models.CharField(default=0, max_length=15)),
                ('cotaP2', models.CharField(default=0, max_length=15)),
                ('cotaX', models.CharField(default=0, max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Fotbal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tara', models.CharField(max_length=50)),
                ('liga', models.CharField(max_length=50)),
                ('runda', models.CharField(max_length=3)),
                ('data', models.CharField(max_length=50)),
                ('participant1', models.CharField(max_length=50)),
                ('participant2', models.CharField(max_length=50)),
                ('scor', models.CharField(max_length=5)),
                ('rezultat', models.CharField(max_length=50)),
                ('favorita', models.CharField(max_length=50)),
                ('bookmaker_odds', models.ManyToManyField(default=0, to='data.bookmakers')),
            ],
        ),
    ]
