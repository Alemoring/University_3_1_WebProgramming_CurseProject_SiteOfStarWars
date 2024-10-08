from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

from starwars.models import Character
from starwars.serializers import CharacterSerializer

class CharactersViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer