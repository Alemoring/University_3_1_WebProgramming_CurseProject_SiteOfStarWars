from django.contrib import admin

from starwars.models import Character, Fraction, Planet, Race, Starship

# Register your models here.
@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ['name', 'fraction', 'race']
@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'homePlanet']

@admin.register(Fraction)
class FractionAdmin(admin.ModelAdmin):
    list_display = ['name', 'periodInLive']

@admin.register(Planet)
class PlanetAdmin(admin.ModelAdmin):
    list_display = ['name', 'population']

@admin.register(Starship)
class StarshipAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'crew']