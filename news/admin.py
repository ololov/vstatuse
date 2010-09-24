# -*- coding: utf-8 -*-
#
#       Copyright 2010 Yegor Kowalew <kw@sdesign.com.ua>
#
from news.models import News
from django.contrib import admin

class NewsAdmin(admin.ModelAdmin):
    fieldsets = [
    ('Основное',   {'fields': ['header', 'body',]}),
    ]
    list_display = ('header',)

admin.site.register(News, NewsAdmin)
