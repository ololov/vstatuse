# -*- coding: utf-8 -*-
#
#       Copyright 2010 Yegor Kowalew <kw@sdesign.com.ua>
#
from django.db import models

class News(models.Model):
    '''Новости'''
    header = models.CharField(max_length=140, verbose_name=u'Заголовок')
    body = models.TextField(max_length=500, verbose_name='Текст новости')
    date = models.DateTimeField(auto_now=True, verbose_name=u'Дата публикации')

    def __unicode__(self):
        return self.header

    def get_absolute_url(self):
        return "/news/%s/" % self.id

    class Meta:
        verbose_name = "новость"
        verbose_name_plural = "новости"
