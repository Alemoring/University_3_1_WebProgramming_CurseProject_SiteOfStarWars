from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework import serializers
from starwars.models import Character, Starship, Race, Fraction, Planet
from starwars.serializers import CharacterSerializer, StarshipDeleteSerializer, StarshipSerializer, CharacterCreateSerializer, UserSerializer
from starwars.serializers import RaceSerializer, RaceCreateSerializer, FractionSerializer, PlanetSerializer
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Min, Max

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
     
class UsersViewset(mixins.ListModelMixin, GenericViewSet):
     queryset = User.objects.all()
     serializer_class = UserSerializer

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
        
        # Фильтрация по юзеру с помощью параметров url
        username = self.request.query_params.get('username')
        if username is not None:
            qs = qs.filter(user=username)
        # фильтруем по текущему юзеру, если текущий пользователь не супер
        user = self.request.user
        if user.is_superuser == False:
            qs = qs.filter(user=self.request.user)
        return qs
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()
    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        stats = Character.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id")
        )
        print(stats)
        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)
    

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
        
        # Фильтрация по юзеру с помощью параметров url
        username = self.request.query_params.get('username')
        if username is not None:
            qs = qs.filter(user=username)
        # фильтруем по текущему юзеру, если текущий пользователь не супер
        user = self.request.user
        if user.is_superuser == False:
            qs = qs.filter(user=self.request.user)
        return qs
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()
    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        stats = Starship.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id")
        )
        print(stats)
        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)

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
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()
    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        stats = Race.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id")
        )
        print(stats)
        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)

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
        return qs
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()
    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        stats = Fraction.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id")
        )
        print(stats)
        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)
    

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
        return qs
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()
    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        stats = Planet.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id")
        )
        print(stats)
        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)