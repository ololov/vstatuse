# -*- coding: utf-8 -*-
#
#       Copyright 2010 Yegor Kowalew <kw@sdesign.com.ua>
#       Статусы

from django.db import models
from django.contrib.auth.models import User

STATUS_STATUS = (
    ('d', 'Не утверждена'),
    ('p', 'Утверждена'),
)

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
