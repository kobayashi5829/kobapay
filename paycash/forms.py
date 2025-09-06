from django import forms
from .models import Deal

class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ('amount', 'content')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)