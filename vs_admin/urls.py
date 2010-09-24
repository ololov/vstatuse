# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^vs-admin/all/(?P<status_id>[\-\d\w]+)/$', 'vs_admin.views.all'),
    (r'^vs-admin/this/(?P<status_id>[\-\d\w]+)/$', 'vs_admin.views.this'),
    (r'^vs-admin/category/add/$', 'vs_admin.views.add_category'),
    (r'^vs-admin/category/recalculate/$', 'vs_admin.views.category_recalculate'),
    (r'^vs-admin/news/add/$', 'vs_admin.views.add_news'),

)
