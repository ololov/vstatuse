# -*- coding: utf-8 -*-
#
#       Copyright 2010 Yegor Kowalew <kw@sdesign.com.ua>
#
import re
from datetime import *
from random import *
from customuser.models import CustomUser
from status.models import VStatus, RandomText, Category
from django.shortcuts import HttpResponse, render_to_response, HttpResponseRedirect

def unescape(text):
    """Removes HTML or XML character references
       and entities from a text string"""
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # Character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                print "Error with encoding HTML entities"
                pass
        else:
            # Named entity
            text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

def add_base(request):
    '''Добавление в базу статусов из старой базы'''
    from status.old_status import aa
    report_text = 'Так же нужно <a href="/set-ratings/">пересчитать</a> рейтинги!!!<br> <b>Добавлено:</b><br>'
    b = r'(?P<xx>,|\.)(?P<yy>[^\s\W])'
    st = 0
    for ee in aa.split("),("):
        text = ee.split("','")[2]
        text = re.sub('<[^>]+>', '', text.replace("\\", ""))
        if len(text) < 140:
            if '&#' not in text:
                text = re.sub(b, "\g<xx> \g<yy>",  text)
                st+=1
                st_add = unescape(ee.split("','")[5])
                #try:
                    #add_user = CustomUser.objects.get(username=st_add) ###
                #except:
                    #test_mail = st_add + '@testuser.com'
                    #test_pass = st_add + 'pass'
                    #add_user = CustomUser(username=st_add, provider='http://vkontakte.ru/', photo='', identity='')
                    #add_user.save()

                new_status = VStatus(
                    status_text = text,
                    status_status = 'p',
                    status_vote_yes = 0,
                    status_rating = 0,
                    status_vote_no = 0,
                    status_date = ee.split("','")[1],
                    #status_author = add_user
                    )
                new_status.save()
                report_text += "№:" + '<b>' + str(st) + '</b>' + ' ' + text + '<br>'
    return HttpResponse(report_text)

def set_ratings(request):
    '''Пересчет рейтингов статусов и рейтингов пользователей'''
    all_st = VStatus.objects.all()
    all_status_count_p = VStatus.objects.filter(status_status='p').count()
    all_users = CustomUser.objects.all()

    report_text = '<b>Рейтинги статусов:</b> <br>'
    for new_st in all_st:
        new_st.status_rating = round(((new_st.status_vote_yes+new_st.status_vote_no)*100.)/all_status_count_p, 2)
        print new_st.id, new_st.status_text, new_st.status_rating
        report_text += "№:" + '<b>' + str(new_st.id) + '</b>' + ' ' + new_st.status_text.encode("UTF-8") + ' <b>' + str(new_st.status_rating) + '</b><br>'
        new_st.save()

    report_text2 = '<b>Рейтинги авторов:</b> <br>'
    for this_user in all_users:
        votes_yes = 0
        votes_no = 0
        autor_rating = 0.0
        user_status = VStatus.objects.filter(status_author = this_user)
        for st in user_status:
            votes_yes = votes_yes + st.status_vote_yes
            votes_no = votes_no + st.status_vote_no
        try:
            autor_rating = round(((votes_yes-votes_no)*100.)/all_status_count_p, 2)
        except:
            autor_rating = 0.0

        this_user.max_votes_yes = votes_yes
        this_user.max_votes_no = votes_no
        this_user.user_rating = autor_rating
        this_user.status_count = user_status.count()
        this_user.save()

        #print votes_yes, votes_no, autor_rating
        report_text2 += '<b>' +  this_user.username.encode("UTF-8") + ':</b> За: ' + str(votes_yes) + ' Против: ' + str(votes_no) + ' Рейтинг: ' + str(autor_rating) +'<br>'

    return HttpResponse(report_text2 + report_text)

