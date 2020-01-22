from django import forms
from .models import List

class ListForm(forms.ModelForm):
    currency_code = forms.CharField(max_length=3, min_length=3, widget=forms.TextInput(attrs={'placeholder': 'ISO 4217 CODE'}))

    class Meta:
        model = List
        exclude = []