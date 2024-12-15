from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from starwars.models import Character, Starship, Race, Fraction, Planet
from starwars.serializers import CharacterSerializer, StarshipDeleteSerializer, StarshipSerializer, CharacterCreateSerializer
from starwars.serializers import RaceSerializer, RaceCreateSerializer, FractionSerializer, PlanetSerializer

class UserProfileViewSet(GenericViewSet):
	@action(url_path="info", detail=False, methods=["GET"])
	def get_url(self, request, *args, **kwargs):
		user = request.user
		data = {
			"is_authenticated" : user.is_authenticated
		}
		if user.is_authenticated:
			data.update({
				"is_superuser" : user.is_superuser,
				"name" : user.username
			})
		return Response(data)

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
    def get_queryset(self):
        qs = super().get_queryset()
        
        # фильтруем по текущему юзеру
        user = self.request.user
        if user.is_superuser == False:
            qs = qs.filter(user=self.request.user)

        return qs
    

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
    def get_queryset(self):
        qs = super().get_queryset()
        
        # фильтруем по текущему юзеру
        user = self.request.user
        if user.is_superuser == False:
            qs = qs.filter(user=self.request.user)

        return qs

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
    def get_queryset(self):
        qs = super().get_queryset()
        
        

        return qs

class FractionViewSet(mixins.ListModelMixin, 
                        mixins.CreateModelMixin, 
                        mixins.UpdateModelMixin, 
                        mixins.RetrieveModelMixin, 
                        GenericViewSet, 
                        mixins.DestroyModelMixin, ):
    queryset = Fraction.objects.all()
    serializer_class = FractionSerializer
    def get_queryset(self):
        qs = super().get_queryset()
        
        # фильтруем по текущему юзеру
        

        return qs
    

class PlanetViewSet(mixins.ListModelMixin, 
                        mixins.CreateModelMixin, 
                        mixins.UpdateModelMixin, 
                        mixins.RetrieveModelMixin, 
                        GenericViewSet, 
                        mixins.DestroyModelMixin, ):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    def get_queryset(self):
        qs = super().get_queryset()
        
        # фильтруем по текущему юзеру
        

        return qs