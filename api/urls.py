from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes),
    path('vesti-osnovne-studije/<int:broj_vesti>', views.get_vesti_os),
    path('poslednja-vest-osnovne-studije', views.get_poslednja_vest_os),
    path('vesti-semestar/<int:broj_semestra>', views.get_vesti_semestar),
    path('poslednja-vest-predmet/<str:slug>', views.get_poslednja_vest_predmet),
    path('vesti-predmet/<str:slug>/<int:broj_vesti>', views.get_vesti_predmet),
    path('izvori', views.get_izvori),
]