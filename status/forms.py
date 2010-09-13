# -*- coding: utf-8 -*-
#
#       Copyright 2010 Yegor Kowalew <kw@sdesign.com.ua>
#

from django import forms
from django.forms import ModelForm, Textarea, CheckboxSelectMultiple
from status.models import Category, VStatus

class AddStatusForm(ModelForm):
    #status_text = forms.CharField(required=False, widget=forms.Textarea, label=u'Текст статуса')
    #status_source = forms.CharField(required=False)
    status_category =  forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple, label=u'Категории')
    class Meta:
        model = VStatus
        fields = ('status_text', 'status_category')
        widgets = {
            'status_text': Textarea(attrs={'cols': 80, 'rows': 10, 'label':u'Текст статуса'}),
            #'status_category': CheckboxSelectMultiple(attrs={'label':u'Категории'}, help_text=""),
        }
