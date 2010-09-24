# -*- coding: utf-8 -*-
#
#       Copyright 2010 Yegor Kowalew <kw@sdesign.com.ua>
#

from django.shortcuts import HttpResponse, render_to_response, HttpResponseRedirect
from django.contrib.flatpages.models import FlatPage
from django.template.context import RequestContext
from status.views import def_values
from django.http import Http404

def small_help(request):
    try:
        page = FlatPage.objects.get(url='/small-help/')
    except ValueError:
        raise Http404

    dict = {'flatpage':page,
        }
    dict2 = def_values(request).copy()
    dict2.update(dict)
    return render_to_response('flatpages/default.html', dict2, context_instance=RequestContext(request))
