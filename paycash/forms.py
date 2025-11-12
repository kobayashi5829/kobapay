from django import forms
from .models import Deal

class BankDealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ('amount', 'content')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class UserDealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ('amount', 'deal_user', 'content')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)