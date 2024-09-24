from typing import Any
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from starwars.models import Jedi

# Create your views here.
class ShowJedisView(TemplateView):
    template_name ="jedis/show_jedis.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["jedis"] = Jedi.objects.all()
        return context
    