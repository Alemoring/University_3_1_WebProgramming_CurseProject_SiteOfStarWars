from django.contrib import admin

from starwars.models import Jedi, Race

# Register your models here.
@admin.register(Jedi)
class JediAdmin(admin.ModelAdmin):
    list_display = ['name', 'padavan', 'race']
@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'homePlanet']