from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

from starwars.models import Character, Starship, Race, Fraction, Planet
from starwars.serializers import CharacterSerializer, StarshipSerializer, CharacterCreateSerializer, RaceSerializer, FractionSerializer, PlanetSerializer

class CharactersViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    def get_serializer_class(self):
        if self.action == "create":
            return CharacterCreateSerializer
        return self.serializer_class
    

class StarshipViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Starship.objects.all()
    serializer_class = StarshipSerializer

class RaceViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Race.objects.all()
    serializer_class = RaceSerializer