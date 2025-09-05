from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Deal

class IndexView(generic.TemplateView):
    template_name = "index.html"

class HomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = "home.html"

class HistoryView(LoginRequiredMixin, generic.ListView):
    model = Deal
    template_name = 'history.html'

    def get_queryset(self):
        deals = Deal.objects.filter(user=self.request.user).order_by('-updated_at')
        return deals