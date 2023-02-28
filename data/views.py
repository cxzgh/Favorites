from django.shortcuts import render
from .models import Fotbal, Tennis, Baschet
from .fotbal_script import get_fotbal_data
from .tennis_script import get_tennis_data
from .baschet_script import get_baschet_data
from django.db.models import F


# Create your views here.
def home(request):
    if request.method == "POST":
        if 'fotbal' in request.POST.keys():
            get_fotbal_data()
        elif 'tennis' in request.POST.keys():
            get_tennis_data()
        elif 'baschet' in request.POST.keys():
            get_baschet_data()
    return render(request, 'data/home.html')


def fotbal_romania_superliga(request):
    romania_superliga = Fotbal.objects.filter(tara__icontains='ROMÂNIA').order_by(-F('runda'))
    context = {
        'fotbal': romania_superliga,
    }
    return render(request, 'data/fotbal.html', context)


def fotbal_anglia_premier_league(request):
    premier_league = Fotbal.objects.filter(tara__icontains='ANGLIA').order_by(-F('runda'))
    context = {
        'fotbal': premier_league,
    }
    return render(request, 'data/fotbal.html', context)


def fotbal_franta_ligue1(request):
    ligue1 = Fotbal.objects.filter(tara__icontains='FRANŢA').order_by(-F('runda'))
    context = {
        'fotbal': ligue1,
    }
    return render(request, 'data/fotbal.html', context)


def fotbal_germania_bundesliga(request):
    bundesliga = Fotbal.objects.filter(tara__icontains='GERMANIA').order_by(-F('runda'))
    context = {
        'fotbal': bundesliga,
    }
    return render(request, 'data/fotbal.html', context)


def fotbal_italia_serie_a(request):
    serie_a = Fotbal.objects.filter(tara__icontains='ITALIA').order_by(-F('runda'))
    context = {
        'fotbal': serie_a,
    }
    return render(request, 'data/fotbal.html', context)


def fotbal_spania_laliga(request):
    laliga = Fotbal.objects.filter(tara__icontains='SPANIA').order_by(-F('runda'))
    context = {
        'fotbal': laliga,
    }
    return render(request, 'data/fotbal.html', context)


def tenis_australian_open(request):
    australian_open = Tennis.objects.filter(liga__icontains='AUSTRALIAN OPEN').order_by(-F('runda'))
    context = {
        'tennis': australian_open,
    }
    return render(request, 'data/tennis.html', context)


def tenis_french_open(request):
    french_open = Tennis.objects.filter(liga__icontains='FRENCH OPEN').order_by(-F('runda'))
    context = {
        'tennis': french_open,
    }
    return render(request, 'data/tennis.html', context)


def tenis_us_open(request):
    us_open = Tennis.objects.filter(liga__icontains='US OPEN').order_by(-F('runda'))
    context = {
        'tennis': us_open,
    }
    return render(request, 'data/tennis.html', context)


def tenis_wimbledon(request):
    wimbledon = Tennis.objects.filter(liga__icontains='WIMBLEDON').order_by(-F('runda'))
    context = {
        'tennis': wimbledon,
    }
    return render(request, 'data/tennis.html', context)


def baschet_franta_lnb(request):
    lnb = Baschet.objects.filter(tara__icontains='FRANŢA').order_by(-F('runda'))
    context = {
        'baschet': lnb,
    }
    return render(request, 'data/baschet.html', context)


def baschet_italia_liga_a(request):
    liga_a = Baschet.objects.filter(tara__icontains='ITALIA').order_by(-F('runda'))
    context = {
        'baschet': liga_a,
    }
    return render(request, 'data/baschet.html', context)


def baschet_romania_divizia_a(request):
    diviza_a = Baschet.objects.filter(liga__icontains='DIVIZIA A').order_by(-F('runda'))
    context = {
        'baschet': diviza_a,
    }
    return render(request, 'data/baschet.html', context)


def baschet_romanian_cup(request):
    romanian_cup = Baschet.objects.filter(liga__icontains='ROMANIAN CUP').order_by(-F('runda'))
    context = {
        'baschet': romanian_cup,
    }
    return render(request, 'data/baschet.html', context)


def baschet_spania_acb(request):
    acb = Baschet.objects.filter(tara__icontains='SPANIA').order_by(-F('runda'))
    context = {
        'baschet': acb,
    }
    return render(request, 'data/baschet.html', context)


def baschet_sua_nba(request):
    nba = Baschet.objects.filter(tara__icontains='SUA').order_by(-F('runda'))
    context = {
        'baschet': nba,
    }
    return render(request, 'data/baschet.html', context)

