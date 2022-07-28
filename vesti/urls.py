from unicodedata import name
from django.urls import path
from .views import izbor_semestra, VestiOSView, vesti_4semestar, vesti_jednog_predmeta


urlpatterns = [
    # path('popuni', popuni, name='popuni'),
    path('', VestiOSView.as_view(), name='pocetna'),
    path('izbor-semestra', izbor_semestra, name='izbor-semestra'),
    path('cetvrti', vesti_4semestar, name='cetvrti'),
    path('predmet/<str:slug>', vesti_jednog_predmeta)
]
