from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

from starwars.models import Character, Starship, Race, Fraction, Planet
from starwars.serializers import CharacterSerializer, StarshipDeleteSerializer, StarshipSerializer, CharacterCreateSerializer
from starwars.serializers import RaceSerializer, RaceCreateSerializer, FractionSerializer, PlanetSerializer

class CharactersViewset(mixins.ListModelMixin, 
                        mixins.CreateModelMixin, 
                        mixins.UpdateModelMixin, 
                        mixins.RetrieveModelMixin, 
                        GenericViewSet, 
                        mixins.DestroyModelMixin, ):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    def get_serializer_class(self):
        if self.action == "create" or self.action == "delete":
            return CharacterCreateSerializer
        return self.serializer_class
    

class StarshipViewset(mixins.ListModelMixin, 
                        mixins.CreateModelMixin, 
                        mixins.UpdateModelMixin, 
                        mixins.RetrieveModelMixin, 
                        GenericViewSet, 
                        mixins.DestroyModelMixin, ):
    queryset = Starship.objects.all()
    serializer_class = StarshipSerializer
    def get_serializer_class(self):
        if self.action == "create" or self.action == "delete":
            return StarshipDeleteSerializer
        return self.serializer_class

class RaceViewset(mixins.ListModelMixin, 
                        mixins.CreateModelMixin, 
                        mixins.UpdateModelMixin, 
                        mixins.RetrieveModelMixin, 
                        GenericViewSet, 
                        mixins.DestroyModelMixin,):
    queryset = Race.objects.all()
    serializer_class = RaceSerializer
    def get_serializer_class(self):
        if self.action == "create" or self.action == "delete":
            return RaceCreateSerializer
        return self.serializer_class

class FractionViewSet(mixins.ListModelMixin, 
                        mixins.CreateModelMixin, 
                        mixins.UpdateModelMixin, 
                        mixins.RetrieveModelMixin, 
                        GenericViewSet, 
                        mixins.DestroyModelMixin, ):
    queryset = Fraction.objects.all()
    serializer_class = FractionSerializer
    

class PlanetViewSet(mixins.ListModelMixin, 
                        mixins.CreateModelMixin, 
                        mixins.UpdateModelMixin, 
                        mixins.RetrieveModelMixin, 
                        GenericViewSet, 
                        mixins.DestroyModelMixin, ):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer