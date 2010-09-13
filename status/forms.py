# -*- coding: utf-8 -*-
#
#       Copyright 2010 Yegor Kowalew <kw@sdesign.com.ua>
#

from django import forms
from django.forms import ModelForm
from status.models import Category

class AddStatusForm(forms.Form):
    status_text = forms.CharField(required=False, widget=forms.Textarea, label=u'Текст статуса')
    #status_source = forms.CharField(required=False)
    status_category =  forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple, label=u'Категории')
