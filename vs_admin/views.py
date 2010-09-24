# -*- coding: utf-8 -*-
#
#       Copyright 2010 Yegor Kowalew <kw@sdesign.com.ua>
#
from status.views import user_best_cookies, def_values, index, not_zero
from status.models import VStatus, Category#, RandomText,
from customuser.models import CustomUser
from django.core.paginator import Paginator
from django.shortcuts import HttpResponse, render_to_response, HttpResponseRedirect
from django.template.context import RequestContext
from vs_admin.forms import EditorForm, CategoryForm, NewsForm

import re
from django.core.context_processors import csrf

def return_form(request):
    try:
        edit_status = VStatus.objects.filter(status_status='d').order_by('?')[0]
        form = EditorForm(instance=edit_status).as_p()
        dict = {'st': edit_status,
                'form': form,
                'edit_link': 'all',
                'title':'Статус #' + str(edit_status.id).encode("UTF-8"),
            }
        dict2 = def_values(request).copy()
        dict2.update(dict)
        return render_to_response('vs_admin/template_this_status.html', dict2, context_instance=RequestContext(request))
    except:
        error_message = 'Нет не подтвержденных статусов'
        message_type = 'info'
        return index(request, error_message, message_type)

def all(request, status_id):
    c = {}
    c.update(csrf(request))
    if status_id == 'start':
        try:
            status_id = VStatus.objects.filter(status_status='d').order_by('?')[0].id
        except:
            error_message = 'Нет не подтвержденных статусов'
            message_type = 'info'
            return index(request, error_message, message_type)

    if request.user.is_superuser:
        if request.method == 'POST':
            edit_status = VStatus.objects.get(id=status_id)
            form = EditorForm(request.POST, instance=edit_status)
            all_status_count_p = VStatus.objects.filter(status_status='p').count()
            if form.is_valid():
                obj = form.save(commit=False)
                try:
                    obj.status_rating = round(((obj.status_vote_yes+obj.status_vote_no)*100.)/all_status_count_p, 2)
                except:
                    obj.status_rating = 0.0
                obj.save()
                form.save_m2m()
                if obj.status_status == 'p':
                    for category in obj.status_category.all():
                        category = Category.objects.get(id = category.id)
                        category.category_status_count += 1
                        category.save()
                    autor = CustomUser.objects.get(id = obj.status_author.id)
                    if autor.status_count:
                        autor.status_count += 1
                    else:
                        autor.status_count = 1
                    all_st_count = VStatus.objects.filter(status_status='p').count
                    try:
                        if autor.max_votes_yes == None:
                           autor.max_votes_yes = 0
                        if autor.max_votes_no == None:
                           autor.max_votes_no = 0
                        autor.user_rating = round(((autor.max_votes_yes-autor.max_votes_no)*100.)/all_st_count, 2)
                    except:
                        autor.user_rating = 0.0
                    autor.save()

                return return_form(request)
            else:
                dict = {'st': edit_status,
                        'edit_link': 'all',
                        'form': form,
                        'title':'Статус #' + str(edit_status.id).encode("UTF-8"),
                    }
                dict2 = def_values(request).copy()
                dict2.update(dict)
                return render_to_response('vs_admin/template_this_status.html', dict2, context_instance=RequestContext(request))
        else:
            return return_form(request)
    else:
        error_message = 'только суперпользователи пользователи могут юзать админку'
        message_type = 'info'
        return index(request, error_message, message_type)

def this(request, status_id):
    c = {}
    c.update(csrf(request))
    if request.user.is_superuser:
        if request.method == 'POST':
            edit_status = VStatus.objects.get(id=status_id)
            form = EditorForm(request.POST, instance=edit_status)
            all_status_count_p = VStatus.objects.filter(status_status='p').count()
            if form.is_valid():
                obj = form.save(commit=False)
                for category in obj.status_category.all():
                    category = Category.objects.get(id = category.id)
                    category.category_status_count -= 1
                    category.save()
                try:
                    obj.status_rating = round(((obj.status_vote_yes+obj.status_vote_no)*100.)/all_status_count_p, 2)
                except:
                    obj.status_rating = 0.0
                obj.save()
                form.save_m2m()
                if obj.status_status == 'p':
                    for category in obj.status_category.all():
                        category = Category.objects.get(id = category.id)
                        category.category_status_count += 1
                        category.save()
                return HttpResponseRedirect('/')
            else:
                dict = {'st': edit_status,
                        'edit_link': 'this',
                        'form': form,
                        'title':'Статус #' + str(edit_status.id).encode("UTF-8"),
                    }
                dict2 = def_values(request).copy()
                dict2.update(dict)
                return render_to_response('vs_admin/template_this_status.html', dict2, context_instance=RequestContext(request))
        else:
            edit_status = VStatus.objects.get(id=status_id)
            form = EditorForm(instance=edit_status).as_p()
            dict = {'st': edit_status,
                    'edit_link': 'this',
                    'form': form,
                    'title':'Статус #' + str(edit_status.id).encode("UTF-8"),
                }

            dict2 = def_values(request).copy()
            dict2.update(dict)
            return render_to_response('vs_admin/template_this_status.html', dict2, context_instance=RequestContext(request))
    else:
        error_message = 'только суперпользователи пользователи могут юзать админку'
        message_type = 'info'
        return index(request, error_message, message_type)

def add_category(request):
    '''Добавление категории'''
    c = {}
    c.update(csrf(request))
    if request.user.is_superuser:
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/')
            else:
                dict = {'form': form,
                        'title':'Добавление категории',
                    }
                dict2 = def_values(request).copy()
                dict2.update(dict)
                return render_to_response('vs_admin/template_add_category.html', dict2, context_instance=RequestContext(request))
        else:
            form = CategoryForm().as_p()
            dict = {'form': form,
                    'title':'Добавление категории',
                }
            dict2 = def_values(request).copy()
            dict2.update(dict)
            return render_to_response('vs_admin/template_add_category.html', dict2, context_instance=RequestContext(request))
    else:
        error_message = 'только суперпользователи пользователи могут юзать админку'
        message_type = 'info'
        return index(request, error_message, message_type)

def category_recalculate(request):
    """Пересчитать количество статусов в категории"""
    categories =[]
    all_category = Category.objects.all()
    for category in all_category:
        this_category = {}
        this_category['name'] = category.category_name
        this_category['old'] = category.category_status_count
        this_category['new'] = VStatus.objects.filter(status_status = 'p', status_category__id = category.id).count()
        category.category_status_count = this_category['new']
        category.save()
        categories.append(this_category)
    dict = {'status':categories,
            'title':'Категории',
        }
    dict2 = def_values(request).copy()
    dict2.update(dict)
    return render_to_response('vs_admin/template_category_recalculate.html', dict2, context_instance=RequestContext(request))

def add_news(request):
    '''Добавление новости'''
    c = {}
    c.update(csrf(request))
    if request.user.is_superuser:
        if request.method == 'POST':
            form = NewsForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/')
            else:
                dict = {'form': form,
                        'title':'Добавление новости',
                    }
                dict2 = def_values(request).copy()
                dict2.update(dict)
                return render_to_response('vs_admin/template_add_news.html', dict2, context_instance=RequestContext(request))
        else:
            form = NewsForm().as_p()
            dict = {'form': form,
                    'title':'Добавление новости',
                }
            dict2 = def_values(request).copy()
            dict2.update(dict)
            return render_to_response('vs_admin/template_add_news.html', dict2, context_instance=RequestContext(request))
    else:
        error_message = 'только суперпользователи пользователи могут юзать админку'
        message_type = 'info'
        return index(request, error_message, message_type)
