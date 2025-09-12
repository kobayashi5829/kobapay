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
        
        messages.success(self.request, 'Charge取引が完了しました。')
        return super().form_valid(form)
    
class PayView(LoginRequiredMixin, generic.CreateView):
    model = Deal
    template_name = 'pay.html'
    form_class = DealForm
    success_url = reverse_lazy('paycash:history')

    def form_valid(self, form):
        deal = form.save(commit=False)
        deal.user = self.request.user
        deal.deal_type = 'P'
        deal.save()

        user = self.request.user
        user.total_amount -= deal.amount
        user.save()

        messages.success(self.request, 'Pay取引が完了しました。')
        return super().form_valid(form)
    
class UpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Deal
    template_name = 'update.html'
    form_class = DealForm

    def get_success_url(self):
        return reverse_lazy('paycash:detail', kwargs={'pk': self.kwargs['pk']})
    
    def form_valid(self, form):
        user = self.request.user
        before_deal = Deal.objects.get(pk=form.instance.pk)
        after_deal = form.instance

        if before_deal.deal_type == 'C':
            user.total_amount -= before_deal.amount
            user.total_amount += after_deal.amount
            user.save()
        elif before_deal.deal_type == 'P':
            user.total_amount += before_deal.amount
            user.total_amount -= after_deal.amount
            user.save()

        messages.success(self.request, '取引情報を更新しました。')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, '取引情報の更新に失敗しました。')
        return super().form_invalid(form)
    
class DeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Deal
    template_name = 'delete.html'
    success_url = reverse_lazy('paycash:history')

    def form_valid(self, form):
        user = self.request.user
        deal = self.object

        if deal.deal_type == 'C':
            user.total_amount -= deal.amount
            user.save()
        elif deal.deal_type == 'P':
            user.total_amount += deal.amount
            user.save()

        messages.success(self.request, f'取引#{ deal.pk }を削除しました。')
        return super().form_valid(form)