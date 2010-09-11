# -*- coding: utf-8 -*-
#
#       Copyright 2010 Yegor Kowalew <kw@sdesign.com.ua>
#
# Кастомный люзер

from django.db import models

from django.contrib.auth.models import User, UserManager
class CustomUser(User):
    identity = models.CharField(max_length=50, verbose_name='URL идентификатор пользователя', blank=True, null=True)
    provider = models.CharField(max_length=50, verbose_name='URL провайдера', blank=True, null=True)
    uid = models.CharField(max_length=50, verbose_name='uid', blank=True, null=True)
    #nickname = models.CharField(max_length=50, verbose_name='nickname', blank=True, null=True)
    gender = models.CharField(max_length=50, verbose_name='gender', blank=True, null=True)
    photo = models.CharField(max_length=50, verbose_name='photo', blank=True, null=True)
    objects = UserManager()

    class Meta:
        verbose_name = "пользователя"
        verbose_name_plural = "пользователи"
