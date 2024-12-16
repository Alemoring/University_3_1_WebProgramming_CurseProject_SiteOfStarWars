from typing import Any
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from starwars.models import Character

# Create your views here.
class ShowCharactersView(TemplateView):
    template_name ="characters/show_characters.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["characters"] = Character.objects.all()
        return context


class UserListView(View):
    def get(self, request):
        usernames = User.objects.values_list('username', flat=True)
        return Response(usernames)