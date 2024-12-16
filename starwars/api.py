from django.core.cache import cache
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
from rest_framework.permissions import BasePermission
from django.contrib.auth import authenticate, login, logout
import pyotp
import time
import smtplib as smtp

# login = 'morgunov.2004.list.ru@gmail.com'
# password = 'dcqt hsby mbtc whes'

# server = smtp.SMTP('smtp.gmail.com', 587)
# server.starttls()
# server.login(login, password)

# subject = 'TOTP Key'
# text = ''

# server.sendmail(login, 'адрес получателя', f'Subject:{subject}\n{text}')

class UserProfileViewSet(GenericViewSet):
    class OTPSerializer(serializers.Serializer):
        key = serializers.CharField()

    class OTPRequired(BasePermission):
        def has_permission(self, request, view):
            return bool(request.user and cache.get('otp_good', False))
        
	# @action(url_path="info", detail=False, methods=["GET"])
	# def get_url(self, request, *args, **kwargs):
	# 	user = request.user
	# 	data = {
	# 		"is_authenticated" : user.is_authenticated
	# 	}
	# 	if user.is_authenticated:
	# 		data.update({
	# 			"is_superuser" : user.is_superuser,
	# 			"name" : user.username
	# 		})
	# 	return Response(data)
    
    @action(detail=False, url_path="check-login", methods=['GET'])
    def get_check_login(self, request, *args, **kwargs):
        user = request.user
        data = {"is_authenticated": user.is_authenticated}
        if user.is_authenticated:
            data.update({
				"is_superuser" : user.is_superuser,
				"name" : user.username
			})
        return Response(data)
    
    @action(detail=False, url_path="login", methods=['POST'])
    def use_login(self, request, *args, **kwargs):
        userinfo = request.data
        user=authenticate(username=userinfo["username"], password=userinfo["password"])
        if user:
            login(request, user)
        return Response({
            'is_authenticated': bool(user)
        })
    
    @action(detail=False, url_path="logout", methods=['GET'])
    def use_logout(self, request, *args, **kwargs):
        logout(request)
        user = request.user
        return Response({
            'is_authenticated': bool(user)
        })

    @action(detail=False, url_path='otp-login', methods=['POST', "GET"], serializer_class=OTPSerializer)
    def otp_login(self, *args, **kwargs):
        totp = pyotp.TOTP(self.request.user.username) # opt_key
        print(totp.now())
        if(self.request.method == "GET"):
            login = 'morgunov.2004.list.ru@gmail.com'
            password = 'dcqt hsby mbtc whes'

            server = smtp.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(login, password)

            subject = 'TOTP Key'
            text = totp.now()

            server.sendmail(login, 'morgunov2004@list.ru', f'Subject:{subject}\n{text}')
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        success = False
        if totp.now() == serializer.validated_data['key']:
            cache.set('otp_good', True, 60)
            success = True

        return Response({
            'success': success
        })
    
    @action(detail=False, url_path='otp-status')
    def get_otp_status(self, *args, **kwargs):
        otp_good = cache.get('otp_good', False)
        return Response({
            'otp_good': otp_good
        })
    
    @action(detail=False, url_path='otp-required', permission_classes=[OTPRequired])
    def page_with_otp_required(self, *args, **kwargs):
        return Response({
            'success': True
        })
     
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