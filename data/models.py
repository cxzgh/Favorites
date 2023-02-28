from django.db import models


# Create your models here.
class Bookmakers(models.Model):
    bookmaker = models.CharField(max_length=50)
    bookmaker_name = models.CharField(max_length=50)
    cotaP1 = models.CharField(max_length=15, default=0)
    cotaP2 = models.CharField(max_length=15, default=0)
    cotaX = models.CharField(max_length=15, default=0)

    def __str__(self):
        return self.bookmaker_name


class Fotbal(models.Model):
    tara = models.CharField(max_length=50)
    liga = models.CharField(max_length=50)
    runda = models.CharField(max_length=3)
    data = models.CharField(max_length=50)
    participant1 = models.CharField(max_length=50)
    participant2 = models.CharField(max_length=50)
    scor = models.CharField(max_length=5)
    rezultat = models.CharField(max_length=50)
    bookmaker_odds = models.ManyToManyField(Bookmakers, default=0)
    favorita = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.liga} {self.runda} {self.participant1} {self.participant2} {self.scor}'


class Tennis(models.Model):
    liga = models.CharField(max_length=50)
    runda = models.CharField(max_length=3)
    data = models.CharField(max_length=50)
    participant1 = models.CharField(max_length=50)
    participant2 = models.CharField(max_length=50)
    scor = models.CharField(max_length=5)
    rezultat = models.CharField(max_length=50)
    bookmaker_odds = models.ManyToManyField(Bookmakers, default=0)
    favorita = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.liga} {self.runda} {self.participant1} {self.participant2} {self.scor}'


class Baschet(models.Model):
    tara = models.CharField(max_length=50)
    liga = models.CharField(max_length=50)
    runda = models.CharField(max_length=3)
    data = models.CharField(max_length=50)
    participant1 = models.CharField(max_length=50)
    participant2 = models.CharField(max_length=50)
    scor = models.CharField(max_length=5)
    rezultat = models.CharField(max_length=50)
    bookmaker_odds = models.ManyToManyField(Bookmakers, default=0)
    favorita = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.liga} {self.runda} {self.participant1} {self.participant2} {self.scor}'
