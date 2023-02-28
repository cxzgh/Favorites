# Generated by Django 4.1.7 on 2023-02-26 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_tennis'),
    ]

    operations = [
        migrations.CreateModel(
            name='Baschet',
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