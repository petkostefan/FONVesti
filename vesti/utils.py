from django.core.mail import send_mail
from django.conf import settings
from korisnici.models import Profil, Interesovanje
from .models import Izvor, Vest


def sacuvaj_novi_post(izvor, lista_novih):
    stari_postovi = [el['link'] for el in Vest.objects.filter(izvor=izvor).order_by('-id').values('link')]
    lista = []

    for nov in lista_novih:
        if nov['link'] not in stari_postovi:
            print(nov['link'])
            nova_vest = Vest.objects.create(**nov)
            print("Sacuvana nova vest", nova_vest)
            lista.append(nova_vest)
    
    return lista


def posalji_mailove(nove_vesti):
    
    for vest in nove_vesti:
        lista_korisnika = [el['profil'] for el in Interesovanje.objects.filter(izvor=vest.izvor).values('profil')]
        lista_mailova = []

        for korisnik in lista_korisnika:
            email = Profil.objects.get(id=korisnik).email
            lista_mailova.append(email)
    
        for mail in lista_mailova:
            naslov = f"Nova vest iz kategorije {vest.izvor}"
            telo = f"Naslov: {vest.naslov} \nLink ka vesti: {vest.link}"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [mail, ]
            send_mail(naslov, telo, email_from, recipient_list)
            print(f'Poslat mail korisniku {mail}')


def posalji_mail_os(vest):
    lista_korisnika = [el['profil'] for el in Interesovanje.objects.filter(izvor=vest.izvor).values('profil')]
    lista_mailova = []

    for korisnik in lista_korisnika:
        email = Profil.objects.get(id=korisnik).email
        lista_mailova.append(email)
    
    for mail in lista_mailova:
        naslov = f"Nova vest iz kategorije {vest.izvor}"
        telo = f"Naslov: {vest.naslov} \nLink ka vesti: {vest.link}"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [mail, ]
        send_mail(naslov, telo, email_from, recipient_list)
        print(f'Poslat mail korisniku {mail}')