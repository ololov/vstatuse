# -*- coding: utf-8 -*-
#
#       Copyright 2010 Yegor Kowalew <kw@sdesign.com.ua>
#
from status.models import *
from django.contrib import admin


#def make_published(modeladmin, request, queryset):
    #queryset.update(post_status='p')
#
#make_published.short_description = u"Сделать опубликованной"
#
#def make_unpublished(modeladmin, request, queryset):
    #queryset.update(post_status='d')
#
#make_unpublished.short_description = u"Сделать черновиком"


#class TextInline(admin.StackedInline):
    #model = TextBlock
    #extra = 1

class VStatusAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Основное',               {'fields': [('status_text', 'status_status', 'status_author')]}),
        ('Дополнительно',          {'classes': ('collapse',), 'fields': [('status_source', 'status_vote_yes_date'), ('status_vote_yes','status_vote_no','status_rating')]}),
    ]
    list_display = ('status_text', 'status_status', 'status_rating')
    search_fields = ['status_text']
    list_filter = ('status_status', 'status_rating', 'status_author')

admin.site.register(VStatus, VStatusAdmin)
