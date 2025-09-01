from django.shortcuts import render

# Create your views here.
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(generic.TemplateView):
    template_name = "index.html"

class HomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = "home.html"