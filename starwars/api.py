from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

from starwars.models import Character, Starship
from starwars.serializers import CharacterSerializer, StarshipSerializer

class CharactersViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer

class StarshipViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Starship.objects.all()
    serializer_class = StarshipSerializer