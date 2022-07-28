from rest_framework import serializers
from vesti.models import Izvor, Vest
from korisnici.models import Interesovanje, Profil


class VestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vest
        fields = '__all__'


class IzvorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Izvor
        fields = '__all__'


class InteresovanjeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interesovanje
        fields = '__all__'


class ProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profil
        fields = '__all__'