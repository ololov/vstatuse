# -*- coding: utf-8 -*-
#
#       Copyright 2010 Yegor Kowalew <kw@sdesign.com.ua>
#

from django.conf.urls.defaults import *
import settings

from django.contrib import admin
admin.autodiscover()

#from django.conf.urls.defaults import *
#handler404 = 'status.views.custom_404_view'
#handler500 = 'status.views.custom_error_view'

from status.sitemap import VSitemap

sitemaps = {
    'site': VSitemap,
}


urlpatterns = patterns('',
    # Example:
    # (r'^vstatuse/', include('vstatuse.foo.urls')),
    #(r'^tag/(?P<tag>[\-\d\w]+)/$', 'post.views.tags_list'),
    #(r'^admin-side/$', 'status.views.admin_side'),
    (r'', include('customuser.urls')),
    (r'', include('vs_admin.urls')),
    (r'', include('news.urls')),

    (r'^add-status/$', 'status.views.add_status'), # надо вынести в другой файл.
    (r'^add-base/$', 'vs_admin.add_db.add_base'),
    (r'^set-ratings/$', 'vs_admin.add_db.set_ratings'),

    (r'^vote/(?P<action>[\-\d\w]+)/(?P<id>[\-\d\w]+)/$', 'status.views.vote'),

    #(r'^source/(?P<source>[\-\d\w]+)$', 'status.views.by_this_source'), # скорее всего выброшу

# Сортировка
    (r'^random-ten/$', 'status.views.random_ten'),

    (r'^rating/(?P<rating>[\-\d\w]+)$', 'status.views.by_this_rating'),
    (r'^date/(?P<this_date>[\-\d\w]+)$', 'status.views.by_this_date'),
    (r'^order-by/best/(?P<ordering>[\-\d\w]+)/(?P<num>[\-\d\w]+)/$', 'status.views.order_best'),
    (r'^order-by/category/(?P<category>[\-\d\w]+)/$', 'status.views.by_category'),

    (r'^order-by/(?P<ordering>[\-\d\w]+)/$', 'status.views.order'),
    (r'^autor/all/$', 'status.views.all_autor'),
    (r'^autor/(?P<autor>[\-\d\w]+)/$', 'status.views.by_autor'),
    (r'^order-by/autor/(?P<autor>[\-\d\w]+)/(?P<yesno>[\-\d\w]+)/$', 'status.views.autor_yes_no'),
    (r'^autor/rating/(?P<rating>[\-\d\w]+)/$', 'status.views.by_autor_rating'),
    (r'^status/(?P<id>[\-\d\w]+)/$', 'status.views.this_status'),


    (r'^$', 'status.views.index'),
    (r'^admin/', include(admin.site.urls)),

    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

    (r'^small-help/$', 'status.flat.small_help'),
    #(r'^test/$', 'twitter.views.tw'),
)

if settings.DEBUG == True:
    if settings.OS_WER == 'W':
        site_media = 'C:/projects/an/stat/'
    else:
        site_media = '/home/yegor/Work/Django/vstatuse/stat/'
    urlpatterns += patterns('',
        (r'^stat/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media}),
    )
