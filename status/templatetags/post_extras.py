# -*- coding: utf-8 -*-
#
#       Copyright 2010 Yegor Kowalew <kw@sdesign.com.ua>
#

from django import template
#from post.models import Section, Tag, Post
import pytils
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
