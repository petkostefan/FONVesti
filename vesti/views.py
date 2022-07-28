from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Vest, Izvor
from .dates import oznaci_nove_postove, ulepsaj_datum, oznaci_tip


class VestiOSView(ListView):
    model = Vest
    paginate_by = 5
    context_object_name = 'posts'
    template_name = 'index.html'

    def get_queryset(self):
        vesti = Vest.objects.filter(izvor=Izvor.objects.get(naziv='Osnovne studije')).order_by('-vreme')
        return oznaci_nove_postove(vesti)
    

def index(request):
    posts = Vest.objects.filter(izvor=Izvor.objects.get(naziv='Osnovne studije')).order_by('-id').values()[:5]
    posts = oznaci_nove_postove(posts)
    context = {
        'posts': posts
    }
    return render(request, 'index.html', context=context)


def izbor_semestra(request):
    return render(request, 'izbor_semestra.html')


def vesti_4semestar(request):
    izvori = Izvor.objects.filter(semestar=4)

    lista_vesti = []
    for izvor in izvori:
        vest = Vest.objects.filter(izvor=izvor).order_by('-vreme')[0]
        vest.vreme = ulepsaj_datum(vest.vreme)
        vest.tip = oznaci_tip(vest.vreme)
        vest.opis = vest.opis[:200] 
        lista_vesti.append(vest)

    context = {'vesti':lista_vesti}
    return render(request, 'vesti_predmet.html', context)


def vesti_jednog_predmeta(request, slug):
    izvor = Izvor.objects.get(slug=slug)
    vesti = Vest.objects.filter(izvor=izvor)

    for vest in vesti:
        vest.vreme = ulepsaj_datum(vest.vreme)
        vest.tip = oznaci_tip(vest.vreme)
        vest.opis = vest.opis[:200] + '...' 

    context = {'vesti':vesti}
    return render(request, 'vesti_predmet.html', context)