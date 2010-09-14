# -*- coding: utf-8 -*-
#
#       Copyright 2010 Yegor Kowalew <kw@sdesign.com.ua>
#

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from customuser.models import CustomUser
#from my_project.authuser.models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'photo', 'status_count', 'user_rating', 'max_votes_yes', 'max_votes_no')

admin.site.unregister(User)
admin.site.register(CustomUser, CustomUserAdmin)

