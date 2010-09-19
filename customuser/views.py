# -*- coding: utf-8 -*-
#
#       Copyright 2010 Yegor Kowalew <kw@sdesign.com.ua>
#

from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
#from post.models import RandomText, Post #Section,#,  Tag, TextBlock, Gallery
from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect
import random
#import logging # Для отладки!
from django.contrib.auth.models import User
from customuser.models import CustomUser
import urllib
import simplejson
from django.contrib.auth import authenticate, login, logout
from customuser.forms import AuthConfirmation
import pytils
@csrf_exempt
def registration_confirm(request):
    """
        'identity':'',
        'provider':'',
        'uid':'',
        'nickname':'',
        'email':'',
        'gender':'',
        'photo':'',
        'full_name':'',
        'first_name':'',
        'middle_name':'',
        'icq':'',
        'jabber':'',
        'skype':'',
        'default':'',
        'blog':'',
        'language':'',
        'biography':'',
        'username':''
    """
    if request.method == 'POST':
        link = 'http://loginza.ru/api/authinfo?token='+request.POST['token']
        f = urllib.urlopen(link)
        json_request = f.read()
        this_user ={}
        for f, key in simplejson.loads(json_request).items():
                if isinstance(key, dict):
                    for a, b in key.items():
                        this_user[a] = b
                else:
                    this_user[f] = key

        user = authenticate(identity = this_user['identity'])
        if user is not None:
            if user.is_active:
                login(request, user)
                user.is_authenticated = True
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/')
        else:
            new_user = CustomUser(
                username = pytils.translit.slugify(this_user['first_name']+'_'+this_user['last_name']),
                identity = this_user['identity'],
                provider = this_user['provider'],
                uid = this_user['uid'],
                gender = this_user['gender'],
                photo = this_user['photo'],
                first_name = this_user['first_name'],
                last_name = this_user['last_name'],
                #is_authenticated = True,
            )
            new_user.save()
            user = authenticate(identity = this_user['identity'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    user.is_authenticated = True
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponseRedirect('/')
            return HttpResponseRedirect('/')

#@csrf_exempt
#def contact_answer(request):
    #if request.method == 'POST':
        #form = AuthConfirmation(request.POST)
        #if form.is_valid():
            #us = CustomUser.objects.get(username = form.cleaned_data['username'])
            #us.email = form.cleaned_data['email']
            #us.is_active = True
            #us.is_authenticated = True
            #us.save()
            #user = authenticate(username = form.cleaned_data['username'], provider = form.cleaned_data['provider'])
            #print user
            #if user is not None:
                #if user.is_active:
                    #login(request, user)
                    #user.is_authenticated = True
                    #return HttpResponseRedirect('/')
#
        #else:
            #default_data = {}
            #default_data['username'] = form.cleaned_data['username']
            #default_data['provider'] = form.cleaned_data['provider']
            #default_data['email'] = form.cleaned_data['email']
            #from django.template import Context, Template
            #t = Template('<b>Вы согласны с этими данными?</b></br><form action="/contact-answer/" method="post">{{ form.as_p }}<input type="submit" value="подтвердить"/></form>')
            #form = AuthConfirmation(default_data)
            #c = Context({"form": form})
            #content = t.render(c)
    #content = 'ogo'
    #return render_to_response('template_contact.html',{
                                #'content':content,
                                #},)

def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

