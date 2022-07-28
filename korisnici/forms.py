from django import forms
from django.forms import ModelForm, widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profil, Interesovanje
from django.db import transaction
from vesti.models import Izvor

class KorisnikRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        korisnik = super().save(commit=False)
        korisnik.save()
        profil = Profil.objects.create(korisnik=korisnik)
        profil.ime = korisnik.first_name
        profil.prezime = korisnik.last_name
        profil.email = korisnik.email
        profil.username = korisnik.username
        profil.save()
        return korisnik


class ProfilForm(ModelForm):
    class Meta:
        model = Profil
        fields = '__all__'


class InteresovanjeForm(forms.Form):
    izvori = forms.ModelMultipleChoiceField(queryset=Izvor.objects.all(), widget=widgets.CheckboxSelectMultiple, label='Izaberite interesovanja')
