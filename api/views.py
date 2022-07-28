from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import VestSerializer, IzvorSerializer
from vesti.models import Izvor, Vest


@api_view(['GET'])
def get_routes(request):

    routes = [
        {'GET': '/api'},
        {'GET': '/api/vesti-osnovne-studije/<int:broj-vesti>'},
        {'GET': '/api/poslednja-vest-osnovne-studije'},
        {'GET': '/api/vesti-semestar/<int:broj>'},
        {'GET': '/api/poslednja-vest-predmet/<str:predmet>'},
        {'GET': '/api/vesti-predmet/<str:predmet>/<int:broj-vesti>'},
        {'GET': '/api/izvori'},
    ]

    return Response(routes)


@api_view(['GET'])
def get_vesti_os(request, broj_vesti):
    vesti = Vest.objects.filter(izvor=Izvor.objects.get(naziv='Osnovne studije')).order_by('-vreme')
    if broj_vesti:
        vesti = vesti[:broj_vesti]
    serializer = VestSerializer(vesti, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_poslednja_vest_os(request):
    vesti = Vest.objects.filter(izvor=Izvor.objects.get(naziv='Osnovne studije')).order_by('-vreme')[0]
    serializer = VestSerializer(vesti, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def get_vesti_semestar(request, broj_semestra):
    izvori = Izvor.objects.filter(semestar=broj_semestra)
    
    lista_vesti = []
    for izvor in izvori:
        vest = vest = Vest.objects.filter(izvor=izvor).order_by('-vreme')[0]
        lista_vesti.append(vest)

    serializer = VestSerializer(lista_vesti, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_poslednja_vest_predmet(request, slug):
    try:
        vest = Vest.objects.filter(izvor=Izvor.objects.get(slug=slug)).order_by('-vreme')[0]
    except:
        return Response([])        
    serializer = VestSerializer(vest, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def get_vesti_predmet(request, slug, broj_vesti):
    try:
        vesti = Vest.objects.filter(izvor=Izvor.objects.get(slug=slug)).order_by('-vreme')
    except:
        return Response([])    
    if broj_vesti:
        vesti = vesti[:broj_vesti]

    serializer = VestSerializer(vesti, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_izvori(request):
    izvori = Izvor.objects.all()
    serializer = IzvorSerializer(izvori, many=True)
    return Response(serializer.data)