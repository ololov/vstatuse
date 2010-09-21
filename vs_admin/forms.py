# -*- coding: utf-8 -*-
#
#       Copyright 2010 Yegor Kowalew <kw@sdesign.com.ua>
#

from django import forms
from django.forms import ModelForm, Textarea, CheckboxSelectMultiple, HiddenInput, DecimalField
from status.models import Category, VStatus

class EditorForm(ModelForm):
    status_category =  forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple, label=u'Категории', required=False)
    class Meta:
        model = VStatus
        fields = ('status_text', 'status_status', 'status_author', 'status_category')
        widgets = {
            'status_text': Textarea(attrs={'cols': 80, 'rows': 10, 'label':u'Текст статуса'}),
        }
