from django.contrib import admin

from starwars.models import Jedi

# Register your models here.
@admin.register(Jedi)
class JediAdmin(admin.ModelAdmin):
    list_display = ['name', 'padavan']