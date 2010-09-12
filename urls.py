# -*- coding: utf-8 -*-
#
#       Copyright 2010 Yegor Kowalew <kw@sdesign.com.ua>
#

from django.conf.urls.defaults import *
import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^vstatuse/', include('vstatuse.foo.urls')),
    #(r'^tag/(?P<tag>[\-\d\w]+)/$', 'post.views.tags_list'),
    #(r'^admin-side/$', 'status.views.admin_side'),
    (r'', include('customuser.urls')),

    (r'^add-status/$', 'status.views.add_status'), # надо вынести в другой файл.
    (r'^add-base/$', 'status.views.add_base'),

    (r'^vote/(?P<action>[\-\d\w]+)/(?P<id>[\-\d\w]+)/$', 'status.views.vote'),

    (r'^source/(?P<source>[\-\d\w]+)$', 'status.views.by_this_source'), # скорее всего выброшу

# Сортировка
    (r'^random-ten/$', 'status.views.random_ten'),
    (r'^rating/(?P<rating>[\-\d\w]+)$', 'status.views.by_this_rating'),
    (r'^date/(?P<this_date>[\-\d\w]+)$', 'status.views.by_this_date'),
    (r'^order-by/best/(?P<ordering>[\-\d\w]+)/(?P<num>[\-\d\w]+)/$', 'status.views.order_best'),
    (r'^order-by/(?P<ordering>[\-\d\w]+)/$', 'status.views.order'),
    (r'^autor/all/$', 'status.views.all_autor'),
    (r'^autor/(?P<autor>[\-\d\w]+)/$', 'status.views.by_autor'),



    (r'^$', 'status.views.index'),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    if settings.OS_WER == 'W':
        site_media = 'C:/projects/an/stat/'
    else:
        site_media = '/home/yegor/Work/Django/vstatuse/stat/'
    urlpatterns += patterns('',
        (r'^stat/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media}),
    )
