from django.db import models
from django.contrib.auth.models import User


class Profil(models.Model):
    korisnik = models.OneToOneField(User, on_delete=models.CASCADE)
    ime = models.CharField(max_length=200)
    prezime = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    username = models.CharField(max_length=200)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = 'profili'
    

class Interesovanje(models.Model):
    profil = models.ForeignKey('Profil', on_delete=models.CASCADE)
    izvor = models.ForeignKey('vesti.Izvor', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.profil} - {self.izvor}'

    class Meta:
        verbose_name_plural = 'interesovanja'