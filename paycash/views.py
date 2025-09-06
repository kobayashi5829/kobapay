from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Deal
from .forms import DealForm

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
    
class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Deal
    template_name = 'detail.html'

class ChargeView(LoginRequiredMixin, generic.CreateView):
    model = Deal
    template_name = 'charge.html'
    form_class = DealForm
    success_url = reverse_lazy('paycash:history')

    def form_valid(self, form):
        deal = form.save(commit=False)
        deal.user = self.request.user
        deal.deal_type = 'C'
        deal.save()

        user = self.request.user
        user.total_amount += deal.amount
        user.save()
        
        messages.success(self.request, 'Chargeが完了しました。')
        return super().form_valid(form)