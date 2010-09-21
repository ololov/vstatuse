# -*- coding: utf-8 -*-
#
#       Copyright 2010 Yegor Kowalew <kw@sdesign.com.ua>
#
# Кастомный люзер

from django.db import models

from django.contrib.auth.models import User, UserManager
class CustomUser(User):
    '''Расширение модели юзера'''
    identity = models.CharField(max_length=50, verbose_name='URL идентификатор пользователя', blank=True, null=True)
    provider = models.CharField(max_length=50, verbose_name='URL провайдера', blank=True, null=True)
    uid = models.CharField(max_length=50, verbose_name='uid', blank=True, null=True)
    gender = models.CharField(max_length=50, verbose_name='gender', blank=True, null=True)
    photo = models.CharField(max_length=100, verbose_name='photo', blank=True, null=True)
    max_votes_yes = models.IntegerField(verbose_name='Всего голосов за', blank=True, null=True)
    max_votes_no = models.IntegerField(verbose_name='Всего голосов против', blank=True, null=True)
    user_rating = models.FloatField(verbose_name='Рейтинг пользователя', blank=True, null=True)
    status_count = models.IntegerField(verbose_name='Всего статусов', blank=True, null=True)
    objects = UserManager()
    class Meta:
        verbose_name = "пользователя"
        verbose_name_plural = "пользователи"
