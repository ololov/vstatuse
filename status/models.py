# -*- coding: utf-8 -*-
#
#       Copyright 2010 Yegor Kowalew <kw@sdesign.com.ua>
#       Статусы

from django.db import models
from django.contrib.auth.models import User
import pytils

def add_zero(value):
    len_val = len(str(value))
    if len_val < 8:
        return '0'*(8-len_val)+str(value)
    return value


STATUS_STATUS = (
    ('d', 'Не подтвержден'),
    ('p', 'Подтвержден'),
    ('r', 'Удален'),
    ('t', 'Мусор'),
)

class RandomText(models.Model):
    '''Подписи в шапке сайта'''
    random_text_body = models.TextField(max_length=50, verbose_name='Текст')
    random_text_status = models.CharField(max_length=1, choices=STATUS_STATUS, verbose_name=u'Статус блока', default='p')

    def __unicode__(self):
        return self.random_text_body

    class Meta:
        verbose_name = "случайный заголовок"
        verbose_name_plural = "Случайные заголовки"

class Category(models.Model):
    '''Модель категорий (тегов)'''
    category_name = models.CharField(max_length=50, verbose_name=u'Название')
    category_slug = models.CharField(max_length=50, verbose_name=u'Служебное поле', unique=True, blank=True)
    category_status_count = models.IntegerField(verbose_name=u'Количество статусов в категории', blank=True, null=True, default=0)
    category_description = models.CharField(max_length=100, verbose_name=u'Описание', blank=True, null=True)

    def save(self):
        if not self.category_slug:
            self.category_slug = pytils.translit.slugify(self.category_name)
        super(Category, self).save()

    def __unicode__(self):
        return self.category_name

    def get_absolute_url(self):
        return "/category/%s/" % self.category_slug

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

class VStatus(models.Model):
    '''Модель статусов'''
    status_text = models.CharField(max_length=140, verbose_name=u'Текст статуса', default=u'Текст нового суперстатуса')
    status_status = models.CharField(max_length=1, choices=STATUS_STATUS, verbose_name=u'Статус cтатуса', default='p')
    status_source = models.CharField(max_length=50, verbose_name=u'Источник', blank=True, null=True)
    status_rating = models.FloatField(verbose_name='Рейтинг', blank=True, null=True, default=0)
    status_vote_yes = models.IntegerField(verbose_name='Голосов "За"', blank=True, null=True, default=0)
    status_vote_yes_date = models.DateField(verbose_name=u'Дата последнего положительного голоса', null=True,blank=True)
    status_vote_no = models.IntegerField(verbose_name='Голосов "Против"', blank=True, null=True, default=0)
    status_date = models.DateField(auto_now=True, verbose_name=u'Дата публикации')
    status_author = models.ForeignKey(User, verbose_name=u'Автор', blank=True, null=True)
    status_category = models.ManyToManyField(Category, verbose_name=u'Категории', blank=True, null=True)

    def __unicode__(self):
        return self.status_text

    def get_edit_url(self):
        return "/vs-admin/this/%d/" % self.id

    def get_absolute_url(self):
        id_zero = add_zero(self.id)
        return "/status/%s/" % id_zero

    class Meta:
        verbose_name = "статус"
        verbose_name_plural = "статусы"
