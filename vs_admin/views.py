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

def alternate_editor(request):
    '''Постатусный редактор'''
    status_id = '0000170'
    edit_status = VStatus.objects.get(id=not_zero(status_id))
    if request.user.is_superuser:
        if request.method == 'POST':
            if form.is_valid():
                print 'то что надо'
            else:
                #print 'не то что надо'
                form = EditorForm().as_p()
                dict = {'st':edit_status,
                        'form': form,
                        'title':'Статус #' + status_id.encode("UTF-8"),
                    }
                dict2 = def_values(request).copy()
                dict2.update(dict)
                return render_to_response('vs_admin/template_this_status.html', dict2, context_instance=RequestContext(request))

        # Если мы просто заходим на страницу
        init = {'status_text': edit_status.status_text,
                'status_status': edit_status.status_status,
                }
        form = EditorForm(init).as_p()
        dict = {'st':VStatus.objects.get(id=not_zero(status_id)),
                'form': form,
                'title':'Статус #' + status_id.encode("UTF-8"),
            }
        dict2 = def_values(request).copy()
        dict2.update(dict)
        return render_to_response('vs_admin/template_this_status.html', dict2, context_instance=RequestContext(request))
    else:
        error_message = 'только авторизированные пользователи могут юзать админку'
        message_type = 'info'
        return index(request, error_message, message_type)
