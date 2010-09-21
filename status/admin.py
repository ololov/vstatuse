# -*- coding: utf-8 -*-
#
#       Copyright 2010 Yegor Kowalew <kw@sdesign.com.ua>
#
from status.models import *
from django.contrib import admin


def make_published(modeladmin, request, queryset):
    queryset.update(status_status='p')

make_published.short_description = u"Сделать опубликованным"
#
def make_unpublished(modeladmin, request, queryset):
    queryset.update(status_status='d')

make_unpublished.short_description = u"Сделать неопубликованным"

class VStatusAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Основное',               {'fields': [('status_text', 'status_status', 'status_author')]}),
        ('Дополнительно',          {'classes': ('collapse',), 'fields': [('status_source', 'status_vote_yes_date'), ('status_vote_yes','status_vote_no','status_rating'), 'status_category']}),
    ]
    list_display = ('status_text', 'status_status', 'status_rating')
    search_fields = ['status_text']
    list_filter = ('status_status', 'status_rating', 'status_author')
    actions = [make_published, make_unpublished]

class RandomTextAdmin(admin.ModelAdmin):
    fieldsets = [
    ('Основное',               {'fields': [('random_text_body', 'random_text_status')]}),
    ]
    list_display = ('random_text_body', 'random_text_status')

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
    ('Основное',               {'fields': [('category_name', 'category_slug')]}),
    ('Дополнительно',          {'classes': ('collapse',), 'fields': ['category_status_count']}),
    ]
    list_display = ('category_name', 'category_slug', 'category_status_count')

admin.site.register(RandomText, RandomTextAdmin)
admin.site.register(VStatus, VStatusAdmin)
admin.site.register(Category, CategoryAdmin)
