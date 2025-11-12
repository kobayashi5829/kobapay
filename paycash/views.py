from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from .models import Deal
from .forms import BankDealForm, UserDealForm

class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        deal = get_object_or_404(Deal, pk=self.kwargs['pk'])
        return self.request.user == deal.user

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
    
class DetailView(LoginRequiredMixin, OnlyYouMixin, generic.DetailView):
    model = Deal
    template_name = 'detail.html'

class ChargeView(LoginRequiredMixin, generic.CreateView):
    model = Deal
    template_name = 'charge.html'
    form_class = BankDealForm
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
    form_class = BankDealForm
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
    
class UpdateView(LoginRequiredMixin, OnlyYouMixin, generic.UpdateView):
    model = Deal
    template_name = 'update.html'
    form_class = BankDealForm

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
    
class DeleteView(LoginRequiredMixin, OnlyYouMixin, generic.DeleteView):
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
    
class SendView(LoginRequiredMixin, generic.CreateView):
    model = Deal
    template_name = 'send.html'
    form_class = UserDealForm
    success_url = reverse_lazy('paycash:history')

    def form_valid(self, form):
        deal = form.save(commit=False)
        deal.user = self.request.user
        deal.deal_type = 'S'
        deal.save()

        user = self.request.user
        user.total_amount -= deal.amount
        user.save()

        messages.success(self.request, 'Pay取引が完了しました。')
        return super().form_valid(form)