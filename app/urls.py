"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from starwars import views

from rest_framework.routers import DefaultRouter
from starwars.api import CharactersViewset, StarshipViewset, RaceViewset, PlanetViewSet, FractionViewSet, UserProfileViewSet, UsersViewset

from django.views.decorators.csrf import csrf_exempt

router = DefaultRouter()
router.register("characters", CharactersViewset, basename="Characters")
router.register("starships", StarshipViewset, basename="Starships")
router.register("races", RaceViewset, basename="Races")
router.register("planets", PlanetViewSet, basename="Planets")
router.register("fractions", FractionViewSet, basename="Fractions")
router.register("user", UserProfileViewSet, basename="User")
router.register("users", UsersViewset, basename="Users")

urlpatterns = [
    path('', views.ShowCharactersView.as_view()),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
