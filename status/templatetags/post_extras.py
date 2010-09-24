# -*- coding: utf-8 -*-
#
#       Copyright 2010 Yegor Kowalew <kw@sdesign.com.ua>
#

from django import template
from status.models import VStatus, Category
from customuser.models import CustomUser
import pytils
#from secret import TWITTER_ON, TWITTER_URL

register = template.Library()

@register.filter(name='date_words')
def date_words(value):
    value = pytils.dt.ru_strftime(u"%d %B %Y года", value, inflected=True)
    return value

@register.filter(name='votes_words')
def votes_words(value):
    word = pytils.numeral.choose_plural(value, (u" раз", u" раза", u" раз"))
    value = str(value) + word
    return value

@register.filter(name='point_to_dash')
def point_to_dash(value):
    return str(value).replace(".", "-")

@register.filter(name='add_zero')
def add_zero(value):
    len_val = len(str(value))
    if len_val < 8:
        return '0'*(8-len_val)+str(value)
    return value

@register.filter(name='all_status_d')
def all_status_d(value):
    return str(value) + '/' + str(VStatus.objects.all().count())

@register.filter(name='status_count')
def status_count(value):
    return VStatus.objects.filter(status_status = value).count()

@register.filter(name='this_admin_status_d')
def this_admin_status_d(value):
    admin = CustomUser.objects.get(username = value)
    return VStatus.objects.filter(status_status = 'd').count()

@register.filter(name='category_count')
def category_count(value):
    return Category.objects.all().count()

#@register.filter(name='if_twitter')
#def if_twitter(value):
    #if TWITTER_ON:
        #return '<a href="' + TWITTER_URL + '">Наш твиттер</a>'
    #else:
        #return ''

