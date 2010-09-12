# -*- coding: utf-8 -*-
#
#       Copyright 2010 Yegor Kowalew <kw@sdesign.com.ua>
#       Статусы

from django.db import models
from django.contrib.auth.models import User
import pytils

STATUS_STATUS = (
    ('d', 'Не утверждена'),
    ('p', 'Утверждена'),
)

class RandomText(models.Model):
    '''Подписи в шапке сайта'''
    random_text_body = models.TextField(max_length=50, verbose_name='Текст')
    random_text_status = models.CharField(max_length=1, choices=STATUS_STATUS, verbose_name=u'Статус блока', default='p')

    def __unicode__(self):
        return self.random_text_body

    class Meta:
        verbose_name = "случайный блок"
        verbose_name_plural = "Случайные блоки"

class Category(models.Model):
    '''Модель категорий (тегов)'''
    category_name = models.CharField(max_length=50, verbose_name=u'Название')
    category_slug = models.CharField(max_length=50, verbose_name=u'Служебное поле', unique=True, blank=True)
    category_status_count = models.IntegerField(verbose_name=u'Количество статусов в категории', blank=True, null=True, default=0)

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
    status_vote_yes = models.IntegerField(verbose_name='Голосов за', blank=True, null=True, default=0)
    status_vote_yes_date = models.DateField(verbose_name=u'Дата последнего положительного голоса', null=True,blank=True)
    status_vote_no = models.IntegerField(verbose_name='Голосов против', blank=True, null=True, default=0)
    status_date = models.DateField(auto_now=True, verbose_name=u'Дата публикации')
    status_author = models.ForeignKey(User, verbose_name=u'Автор')

    def __unicode__(self):
        return self.status_text

    #def get_absolute_url(self):
        #return "/XXXXX/%s/" % self.slug

    #def get_edit_url(self):
        #return "/admin/XXXXX/YYYYYY/%d/" % self.id

    #def get_delete_url(self):
        #return "/admin/XXXXXX/YYYYY/%d/delete/" % self.id

    class Meta:
        verbose_name = "статус"
        verbose_name_plural = "статусы"
