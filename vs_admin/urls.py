# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^vs-admin/all/(?P<status_id>[\-\d\w]+)/$', 'vs_admin.views.all'),
    (r'^vs-admin/this/(?P<status_id>[\-\d\w]+)/$', 'vs_admin.views.this'),

)
