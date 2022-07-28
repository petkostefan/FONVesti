from datetime import datetime
from .models import Izvor, Vest
from .scraper import vesti_osnovne_studije, dms_postovi, stat_postovi, mtr_postovi, spa_postovi, num_postovi, fmir_postovi
from celery import shared_task
from .utils import sacuvaj_novi_post, posalji_mailove, posalji_mail_os


@shared_task
def sacuvaj_nove_postove_os():
    poslednjih_pet = [el['vreme'] for el in \
        list(Vest.objects.filter(izvor=\
        Izvor.objects.get(naziv='Osnovne studije')).values('vreme').order_by('-id'))]
    
    novi = vesti_osnovne_studije()
    novi.reverse()

    dodat = False

    for post in novi:
        if post['vreme'] not in poslednjih_pet:
            post['izvor'] = Izvor.objects.get(naziv='Osnovne studije')
            novi_post = Vest.objects.create(**post)
            dodat = True
            posalji_mail_os(novi_post)
            print(f"Dodat novi post {novi_post}")
            print("Vreme: "+str(datetime.now()))

    if not dodat:
        return 'Nema novih vesti'

@shared_task
def sacuvaj_nove_postove_4sem():
    dms = dms_postovi()
    stat = stat_postovi()
    mtr = mtr_postovi()
    spa = spa_postovi()
    num = num_postovi()
    fmir = fmir_postovi()
    lista = [dms, stat, mtr, spa, num, fmir]

    novi_postovi = []

    for el in lista:
        novi_postovi.extend(sacuvaj_novi_post(el[0]['izvor'],el))

    if novi_postovi:
        posalji_mailove(novi_postovi)
    else:
        return 'Nema novih vesti iz 4. semestra'