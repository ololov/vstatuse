# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^vs-admin/alternate-editor/$', 'vs_admin.views.alternate_editor'),

)
