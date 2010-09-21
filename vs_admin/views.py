# -*- coding: utf-8 -*-
#
#       Copyright 2010 Yegor Kowalew <kw@sdesign.com.ua>
#
from status.views import user_best_cookies, def_values, index, not_zero
from status.models import VStatus#, RandomText, Category
from django.core.paginator import Paginator
from django.shortcuts import HttpResponse, render_to_response, HttpResponseRedirect
from django.template.context import RequestContext
from vs_admin.forms import EditorForm
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
                obj.status_rating = round(((obj.status_vote_yes+obj.status_vote_no)*100.)/all_status_count_p, 2)
                obj.save()
                form.save_m2m()
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
        error_message = 'только авторизированные пользователи могут юзать админку'
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
                obj.status_rating = round(((obj.status_vote_yes+obj.status_vote_no)*100.)/all_status_count_p, 2)
                obj.save()
                form.save_m2m()
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
        error_message = 'только авторизированные пользователи могут юзать админку'
        message_type = 'info'
        return index(request, error_message, message_type)
