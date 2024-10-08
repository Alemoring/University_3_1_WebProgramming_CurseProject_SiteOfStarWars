from django.contrib import admin

from starwars.models import Character, Race

# Register your models here.
@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ['name', 'fraction', 'race']
@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'homePlanet']