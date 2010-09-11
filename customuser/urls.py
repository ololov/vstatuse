# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^contact1/$', 'customuser.views.contact1'),
    (r'^contact-answer/$', 'customuser.views.contact_answer'),
    (r'^auth/$', 'customuser.views.auth'),
    (r'^logout/$', 'customuser.views.user_logout'),
    (r'^registration-confirm/$', 'customuser.views.registration_confirm'),
)
