from django.core.management.base import BaseCommand, CommandError
from vesti.models import Vest, Izvor
from vesti.scraper import (vesti_osnovne_studije, dms_postovi, 
                    stat_postovi, mtr_postovi, spa_postovi, 
                    num_postovi, fmir_postovi)
from vesti.utils import sacuvaj_novi_post

class Command(BaseCommand):
    help = 'Inicijalna priprema baze. Brisanje svih postojecih vesti i cuvanje novih.'

    def handle(self, *args, **options):
        Vest.objects.all().delete()
        Izvor.objects.all().delete()

        Izvor.objects.create(naziv='Diskretne matematičke strukture', slug='diskretne-matematicke-strukture', godina=2, semestar=4)
        Izvor.objects.create(naziv='Numerička analiza', slug='numericka-analiza', godina=2, semestar=4)
        Izvor.objects.create(naziv='Finansijski menadžment i računovodstvo', slug='finansijski-menadzment-i-racunovodstvo', godina=2, semestar=4)
        Izvor.objects.create(naziv='Statistika', slug='statistika', godina=2, semestar=4)
        Izvor.objects.create(naziv='Strukture podataka i algoriitmi', slug='strukture-podataka-i-algoriitmi', godina=2, semestar=4)
        Izvor.objects.create(naziv='Menadžment tehnologije i razvoja', slug='menadzment-tehnologije-i-razvoja', godina=2, semestar=4)
        Izvor.objects.create(naziv='Osnovne studije', slug='', godina=0, semestar=0)

        novi = vesti_osnovne_studije()
        novi.reverse()

        for post in novi:
            post['izvor'] = Izvor.objects.get(naziv='Osnovne studije')
            Vest.objects.create(**post)

        dms = dms_postovi()
        stat = stat_postovi()
        mtr = mtr_postovi()
        spa = spa_postovi()
        num = num_postovi()
        fmir = fmir_postovi()
        lista = [dms, stat, mtr, spa, num, fmir]

        for el in lista:
            sacuvaj_novi_post(el[0]['izvor'],el)

        self.stdout.write(self.style.SUCCESS('Uspesno reinicijalizovana baza'))