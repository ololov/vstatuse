from django import forms
from django.forms import ModelForm
#from models import District

class AuthConfirmation(forms.Form):
    #username = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput)
    provider = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput)
    username = forms.CharField(required=False, label=u'Ник')
    email = forms.CharField(required=False, label=u'Почта')
