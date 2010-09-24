# -*- coding: utf-8 -*-
#
#       Copyright 2010 Yegor Kowalew <kw@sdesign.com.ua>
#

from django.shortcuts import HttpResponse, render_to_response, HttpResponseRedirect
from news.models import News
from django.core.paginator import Paginator
from django.template.context import RequestContext
from status.views import def_values


def all(request):
    '''Все новости'''
    news = News.objects.all().order_by('-date')
    if not news:
        news = []
        this_news = {}
        this_news['header'] = 'йомойо!!!'
        this_news['body'] = 'Представляете, нет еще новостей!'
        news.append(this_news)
    paginator = Paginator(news, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        news = paginator.page(page)
    except (EmptyPage, InvalidPage):
        news = paginator.page(paginator.num_pages)
    dict = {'status':news,
            'title':'Новости',
            'description': 'Новости, vkontakte, вконтакте'
        }
    dict2 = def_values(request).copy()
    dict2.update(dict)
    return render_to_response('news/template_news.html', dict2, context_instance=RequestContext(request))
