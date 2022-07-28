from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginKorisnik, name='login'),
    path('logout/', views.logoutKorisnik, name='logout'),
    path('register/', views.registerKorisnik, name='registracija'),

    path('profil/', views.profil, name='profil'),
    path('profil/interesovanja', views.uredi_interesovanja, name='interesovanja')
]
