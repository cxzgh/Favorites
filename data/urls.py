from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('romania_superliga', views.fotbal_romania_superliga, name='romania_superliga'),
    path('anglia_premier_league', views.fotbal_anglia_premier_league, name='anglia_premier_league'),
    path('franta_ligue1', views.fotbal_franta_ligue1, name='franta_ligue1'),
    path('germania_bundesliga', views.fotbal_germania_bundesliga, name='germania_bundesliga'),
    path('italia_serie_a', views.fotbal_italia_serie_a, name='italia_serie_a'),
    path('spania_laliga', views.fotbal_franta_ligue1, name='spania_laliga'),
    path('australian_open', views.tenis_australian_open, name='australian_open'),
    path('french_open', views.tenis_french_open, name='french_open'),
    path('us_open', views.tenis_us_open, name='us_open'),
    path('wimbledon_open', views.tenis_wimbledon, name='wimbledon'),
    path('franta_lnb', views.baschet_franta_lnb, name='lnb'),
    path('italia_liga_a', views.baschet_italia_liga_a, name='liga_a'),
    path('romania_divizia_a', views.baschet_romania_divizia_a, name='divizia_a'),
    path('romanian_cup', views.baschet_romanian_cup, name='romanian_cup'),
    path('spania_acb', views.baschet_spania_acb, name='acb'),
    path('sua_nba', views.baschet_sua_nba, name='nba'),
]
