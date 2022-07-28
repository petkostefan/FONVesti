from django.core.management.base import BaseCommand
from vesti.models import Vest, Izvor

class Command(BaseCommand):
    help = 'Brisanje poslednjeg posta osnovnih studija'

    def handle(self, *args, **options):
        vest = Vest.objects.filter(izvor=Izvor.objects.get(naziv='Osnovne studije')).last()
        vest.delete()
        self.stdout.write(self.style.SUCCESS('Uspesno izbrisan poslednji post osnovnih studija: ' + str(vest)))