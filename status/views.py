# -*- coding: utf-8 -*-
#
#       Copyright 2010 Yegor Kowalew <kw@sdesign.com.ua>
#
# Для работы этой вьюшки требуются модули pytils, dateutil

from django.shortcuts import HttpResponse, render_to_response#, HttpResponseRedirect
from status.models import VStatus
#from django.contrib.auth.models import User
from customuser.models import CustomUser
from django.core.paginator import Paginator
from django.template.context import RequestContext
import datetime
from dateutil.relativedelta import *
import re
import pytils
from random import *

# Всего статусов, включая не опубликованные
all_status_count = VStatus.objects.all().count()
# Список юзеров
all_user = CustomUser.objects.all()
# Количество опубликованных статусов
all_user_count_p = VStatus.objects.filter(status_status='p').count()
# Количество не опубликованных статусов
all_user_count_d = VStatus.objects.filter(status_status='d').count()

#Store.objects.annotate(min_price=Min('books__price'), max_price=Max('books__price'))

# Создаю список юзеров с количеством статусов
list = []
coll_list = {}
all_user_count = all_user.count() # Всего юзеров
for i in all_user:
    coll_list['name'] = i.username
    coll_list['id'] = i.id
    autor_status = VStatus.objects.filter(status_author = i)
    coll_list['status_count'] = autor_status.count()
    votes_yes = 0
    votes_no = 0
    max_rating = 0
    for st in autor_status:
        votes_yes = votes_yes + st.status_vote_yes
        votes_no = votes_no + st.status_vote_no
        if max_rating < st.status_rating:
            max_rating = st.status_rating
    coll_list['date_joined'] = i.date_joined
    coll_list['votes_no'] = votes_no
    coll_list['votes_yes'] = votes_yes
    coll_list['max_rating'] = max_rating
    try:
        coll_list['autor_rating'] = ((votes_yes-votes_no)*100.)/all_user_count_p
    except:
        coll_list['autor_rating'] = 0.0
    list.append(coll_list)
    coll_list = {}

from operator import itemgetter
user_list = sorted(list, key=itemgetter("status_count"), reverse=True)
#print user_list
def unescape(text):
    """Removes HTML or XML character references
       and entities from a text string

       From Fredrik Lundh
       http://effbot.org/zone/re-sub.htm#unescape-html

       Little bit modified
    """
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

def user_best_cookies(request):
    try:
        yes_votes_list = request.session.get('yes_votes_list')
        yes_votes_list_count = len(yes_votes_list)
        no_votes_list = request.session.get('no_votes_list')
    except:
        yes_votes_list = []
        no_votes_list = []
        yes_votes_list_count = 0
    best_list={}
    best_list['yes_votes_list'] = yes_votes_list
    best_list['no_votes_list'] = no_votes_list
    best_list['yes_votes_list_count'] = yes_votes_list_count
    return best_list

def add_base(request):
    from status.old_status import aa
    from datetime import *
    import time
    #print date.fromtimestamp(randint(1230811167.0, 1277985567.0)) # Рандомная дата

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
                if st_add != 'admin':
                    tru_user = False
                    try:
                        add_user = CustomUser.objects.get(username=st_add) ###
                    except:
                        test_mail = st_add + '@testuser.com'
                        test_pass = st_add + 'pass'
                        add_user = CustomUser(username=st_add, provider='http://vkontakte.ru/', photo='', identity='')
                        add_user.save()
                else:
                    tru_user = True
                    admin_user = randint(1,3)
                    if admin_user == 1:
                        try:
                            add_user = CustomUser.objects.get(username='Yegor Kowalew')
                        except:
                            add_user = CustomUser(username='Yegor Kowalew', provider='http://vkontakte.ru/', photo='http://cs336.vkontakte.ru/u13175215/c_d5dabbe7.jpg', identity='http://vkontakte.ru/id13175215')
                            add_user.save()
                    elif admin_user == 2:
                        try:
                            add_user = CustomUser.objects.get(username='Артём Ватутин')
                        except:
                            add_user = CustomUser(username='Артём Ватутин', provider='http://vkontakte.ru/', photo='http://cs9942.vkontakte.ru/u6135314/c_cd457566.jpg', identity='http://vkontakte.ru/id13175215')
                            add_user.save()

                    elif admin_user == 3:
                        try:
                            add_user = CustomUser.objects.get(username='LaDioS')
                        except:
                            add_user = CustomUser(username='LaDioS', provider='http://vkontakte.ru/', photo='http://cs4186.vkontakte.ru/u13463936/a_6a70f089.jpg', identity='http://vkontakte.ru/id1300000')
                            add_user.save()

                if tru_user:
                    new_status = VStatus(
                    status_text = text,
                    status_status = 'p',
                    status_source = 'old base',
                    status_vote_yes = randint(0, 10),
                    status_vote_yes_date = date.fromtimestamp(randint(1230811167.0, 1277985567.0)),
                    status_rating = 0,
                    status_vote_no = randint(1, 3),
                    status_date = ee.split("','")[1],
                    status_author = add_user
                    )
                else:
                    new_status = VStatus(
                    status_text = text,
                    status_status = 'p',
                    status_source = 'old base',
                    status_vote_yes = 0,
                    status_rating = 0,
                    status_vote_no = 0,
                    status_date = ee.split("','")[1],
                    status_author = add_user
                    )
                new_status.save()
                #return HttpResponse("№:" + str(st))
                print "№:", st, ' ', add_user.username, ' ', text

    all_st = VStatus.objects.all()
    for new_st in all_st:
        new_st.status_rating = round(((new_st.status_vote_yes+new_st.status_vote_no)*100.)/all_user_count_p, 2)
        print new_st.id, new_st.status_rating
        new_st.save()
    return HttpResponse('<b>Добавлено:</b> ' + str(st))

def index(request):
    #from django.db.models import Avg, Max, Min, Count
    #print CustomUser.objects.all()
    #print User.objects.all()
    #from random import *
    #print randint(12, 127)
    #time_tuple = (2010, 07, 01, 13, 59, 27, 2, 317, 0)
    #timestamp = time.mktime(time_tuple)
    #print datetime(*time_tuple[0:6])
    #print timestamp
    #for i in VStatus.objects.values('status_author__username', 'status_vote_yes', 'status_vote_no').annotate(Count('status_author')):
        #print i

    best_cookies = user_best_cookies(request)
    status_list = VStatus.objects.filter(status_status='p').order_by('-status_rating')
    paginator = Paginator(status_list, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        status = paginator.page(page)
    except (EmptyPage, InvalidPage):
        status = paginator.page(paginator.num_pages)
    return render_to_response('template_status.html',{
                                'status':status,
                                'all_status_count':all_status_count,
                                'all_user_count':all_user_count,
                                'title':'по Рейтингу',
                                'all_user':user_list,
                                'all_user_count_p':all_user_count_p,
                                'yes_votes_list':best_cookies['yes_votes_list'],
                                'no_votes_list':best_cookies['no_votes_list'],
                                'yes_votes_list_count':best_cookies['yes_votes_list_count']
                            }, context_instance=RequestContext(request))

def by_this_date(request, this_date):
    import time
    best_cookies = user_best_cookies(request)
    e = this_date.split("-")
    status_list = VStatus.objects.filter(status_status='p', status_date__day=e[2], status_date__month=e[1], status_date__year=e[0]).order_by('-status_rating')
    paginator = Paginator(status_list, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        status = paginator.page(page)
    except (EmptyPage, InvalidPage):
        status = paginator.page(paginator.num_pages)
    return render_to_response('template_status.html',{
                                'status':status,
                                'current':'sort',
                                'all_status_count':all_status_count,
                                'all_user_count':all_user_count,
                                'title':pytils.dt.ru_strftime(u"за %d %B %Y", datetime.datetime.fromtimestamp(time.mktime(time.strptime(this_date, "%Y-%m-%d"))), inflected=True),
                                'all_user':user_list,
                                'all_user_count_p':all_user_count_p,
                                'yes_votes_list':best_cookies['yes_votes_list'],
                                'no_votes_list':best_cookies['no_votes_list'],
                                'yes_votes_list_count':best_cookies['yes_votes_list_count']
                            }, context_instance=RequestContext(request))

def random_ten(request):
    best_cookies = user_best_cookies(request)
    all_status = VStatus.objects.all()
    all_status_count = all_status.count()
    status = []
    for i in xrange(10):
        status.append(all_status[randint(0, all_status_count)])
    return render_to_response('template_status_ten.html',{
                                'status':status,
                                'current':'sort',
                                'all_status_count':all_status_count,
                                'all_user_count':all_user_count,
                                'title':'Случайная десятка',
                                'all_user':user_list,
                                'all_user_count_p':all_user_count_p,
                                'yes_votes_list':best_cookies['yes_votes_list'],
                                'no_votes_list':best_cookies['no_votes_list'],
                                'yes_votes_list_count':best_cookies['yes_votes_list_count']
                            }, context_instance=RequestContext(request))

def by_this_source(request, source):
    '''Оставляю до лучших времен'''
    best_cookies = user_best_cookies(request)
    status_list = VStatus.objects.filter(status_status='p', status_source=source).order_by('-status_rating')
    paginator = Paginator(status_list, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        status = paginator.page(page)
    except (EmptyPage, InvalidPage):
        status = paginator.page(paginator.num_pages)
    return render_to_response('template_status.html',{
                                'status':status,
                                'all_status_count':all_status_count,
                                'all_user_count':all_user_count,
                                'title':'по Дате',
                                'all_user':user_list,
                                'all_user_count_p':all_user_count_p,
                                'yes_votes_list':best_cookies['yes_votes_list'],
                                'no_votes_list':best_cookies['no_votes_list'],
                                'yes_votes_list_count':best_cookies['yes_votes_list_count']
                            }, context_instance=RequestContext(request))

def by_this_rating(request, rating):
    #print rating.replace("-", ".")
    best_cookies = user_best_cookies(request)
    status_list = VStatus.objects.filter(status_status='p', status_rating=rating.replace("-", "."))
    paginator = Paginator(status_list, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        status = paginator.page(page)
    except (EmptyPage, InvalidPage):
        status = paginator.page(paginator.num_pages)
    return render_to_response('template_status.html',{
                                'status':status,
                                'current':'sort',
                                'all_status_count':all_status_count,
                                'all_user_count':all_user_count,
                                'title':'по рейтингу равному '+rating.replace("-", ".").encode("UTF-8"),
                                'all_user':user_list,
                                'all_user_count_p':all_user_count_p,
                                'yes_votes_list':best_cookies['yes_votes_list'],
                                'no_votes_list':best_cookies['no_votes_list'],
                                'yes_votes_list_count':best_cookies['yes_votes_list_count']
                            }, context_instance=RequestContext(request))

def order(request, ordering):
    best_cookies = user_best_cookies(request)
    order_list = [['date','по Дате','-status_date'], ['rating','по Рейтингу','-status_rating'], ['user-top','по Понравившимся','-status_rating']]
    for i in order_list:
        if i[0] == ordering:
            ordering = i
            this_url = i[0]
    #print ordering[1]

    status_list = VStatus.objects.filter(status_status='p').order_by(ordering[2])
    if this_url == 'user-top':
        new_list = []
        for i in best_cookies['yes_votes_list']:
            for y in status_list:
                if i == y.id:
                    new_list.append(y)
        status_list = new_list
    paginator = Paginator(status_list, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        status = paginator.page(page)
    except (EmptyPage, InvalidPage):
        status = paginator.page(paginator.num_pages)

    return render_to_response('template_status.html',{
                                'status':status,
                                'all_status_count':all_status_count,
                                'all_user_count':all_user_count,
                                'title':ordering[1],
                                'all_user':user_list,
                                'all_user_count_p':all_user_count_p,
                                'current':'sort',
                                'yes_votes_list':best_cookies['yes_votes_list'],
                                'no_votes_list':best_cookies['no_votes_list'],
                                'yes_votes_list_count':best_cookies['yes_votes_list_count']
                            }, context_instance=RequestContext(request))

def by_autor(request, autor):
    best_cookies = user_best_cookies(request)

    status_list = VStatus.objects.filter(status_status='p', status_author__id=autor)
    this_username = CustomUser.objects.get(id = autor).username
    paginator = Paginator(status_list, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        status = paginator.page(page)
    except (EmptyPage, InvalidPage):
        status = paginator.page(paginator.num_pages)
    return render_to_response('template_status.html',{
                                'status':status,
                                'all_status_count':all_status_count,
                                'all_user_count':all_user_count,
                                'title':'Автор ' + this_username.encode("UTF-8"),
                                'all_user':user_list,
                                'all_user_count_p':all_user_count_p,
                                'current':'autor',
                                'yes_votes_list':best_cookies['yes_votes_list'],
                                'no_votes_list':best_cookies['no_votes_list'],
                                'yes_votes_list_count':best_cookies['yes_votes_list_count']
                            }, context_instance=RequestContext(request))

def all_autor(request):
    best_cookies = user_best_cookies(request)

    paginator = Paginator(user_list, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        status = paginator.page(page)
    except (EmptyPage, InvalidPage):
        status = paginator.page(paginator.num_pages)

    return render_to_response('template_autors.html',{
                                'status':status,
                                'all_status_count':all_status_count,
                                'all_user_count':all_user_count,
                                'title':'Все пользователи',
                                'all_user':user_list,
                                'all_user_count_p':all_user_count_p,
                                'user_list':list,
                                'current':'autor',
                                'yes_votes_list':best_cookies['yes_votes_list'],
                                'no_votes_list':best_cookies['no_votes_list'],
                                'yes_votes_list_count':best_cookies['yes_votes_list_count']
                            }, context_instance=RequestContext(request))

def add_status(request):
    return render_to_response('template_add_status.html',{
                                #'status':status,
                                'all_status_count':all_status_count,
                                'all_user_count':all_user_count,
                                'title':'Добавление статуса',
                                'all_user':user_list,
                                'all_user_count_p':all_user_count_p,
                                'user_list':list
                            }, context_instance=RequestContext(request))

def vote(request, action, id):
    cookies = request.session
    if action == 'yes':
        if request.session.get('yes_votes_list'):
            cookies['yes_votes_list'].append(int(id))
            cookies.save()
        else:
            cookies['yes_votes_list'] = []
            cookies['yes_votes_list'].append(int(id))
            cookies.save()
        this_status = VStatus.objects.get(id = id)
        this_status.status_vote_yes += 1
        this_status.status_rating = round(((this_status.status_vote_yes+this_status.status_vote_no)*100.)/all_user_count_p, 2)
        status_vote_yes_date = datetime.datetime.now()
        this_status.save()
    elif action == 'no':
        if request.session.get('no_votes_list'):
            cookies['no_votes_list'].append(int(id))
            cookies.save()
        else:
            cookies['no_votes_list'] = []
            cookies['no_votes_list'].append(int(id))
            cookies.save()
        this_status = VStatus.objects.get(id = id)
        this_status.status_vote_no -= 1
        if this_status.status_vote_no == -10:
            this_status.status_status = 'd'

        this_status.status_rating = round(((this_status.status_vote_yes+this_status.status_vote_no)*100.)/all_user_count_p, 2)
        status_vote_yes_date = datetime.datetime.now()
        this_status.save()
    return HttpResponse('')

def order_best(request, ordering, num):
    def fpaginate(date_start, prev, next, next_date, ordering):
        ffpaginate={}
        ffpaginate['title'] = u'Лучшие ' + date_start
        ffpaginate['error'] = u'Пусто, ' + date_start + u' никто не голосовал'
        ffpaginate['this'] = {'date': date_start, 'link':'/order-by/best/' + ordering + '/0'}
        ffpaginate['prev'] = {'date': prev, 'link':'/order-by/best/' + ordering + '/' + str(num + 1)}
        if next_date > datetime.date.today():
            ffpaginate['next'] = {'date': False, 'link':False}
        else:
            ffpaginate['next'] = {'date': next, 'link':'/order-by/best/' + ordering + '/' + str(num - 1)}
        return ffpaginate

    best_cookies = user_best_cookies(request)
    start_day = datetime.date.today()
    num = int(num)
    if ordering == 'day':
        date_start = start_day - relativedelta(days=num)
        status_list = VStatus.objects.filter(status_status='p', status_vote_yes_date=date_start).order_by('-status_rating')[:10]
        start = pytils.dt.ru_strftime(u"за %d %B %Y", date_start, inflected=True)
        date_start = start_day - relativedelta(days=num+1)
        prev = pytils.dt.ru_strftime(u"за %d %B", date_start, inflected=True)
        next_date = start_day - relativedelta(days=num-1)
        next = pytils.dt.ru_strftime(u"за %d %B", next_date, inflected=True)
    elif ordering == 'week':
        date_start = start_day - relativedelta(weeks=num+1)
        date_end = start_day - relativedelta(weeks=num)
        status_list = VStatus.objects.filter(status_status='p', status_vote_yes_date__range=(date_start, date_end)).order_by('-status_rating')[:10]
        start = pytils.dt.ru_strftime(u"c %d %B", date_start, inflected=True) + ', ' + pytils.dt.ru_strftime(u"по %d %B %Y", date_end, inflected=True)
        date_start = start_day - relativedelta(weeks=num+2)
        date_end = start_day - relativedelta(weeks=num+1)
        prev = pytils.dt.ru_strftime(u"c %d %B", date_start, inflected=True) + ', ' + pytils.dt.ru_strftime(u"по %d %B", date_end, inflected=True)
        date_start = start_day - relativedelta(weeks=num)
        next_date = start_day - relativedelta(weeks=num-1)
        next = pytils.dt.ru_strftime(u"c %d %B", date_start, inflected=True) + ', ' + pytils.dt.ru_strftime(u"по %d %B", next_date, inflected=True)
    elif ordering == 'month':
        date_start = start_day - relativedelta(months=+num)
        status_list = VStatus.objects.filter(status_status='p', status_vote_yes_date__month=date_start.month, status_vote_yes_date__year=date_start.year).order_by('-status_rating')[:10]
        start = pytils.dt.ru_strftime(u"за %B %Y", date_start, inflected=False)
        date_start = start_day - relativedelta(months=+(num+1))
        prev = pytils.dt.ru_strftime(u"за %B", date_start, inflected=False)
        next_date = start_day - relativedelta(months=+(num-1))
        next = pytils.dt.ru_strftime(u"за %B", next_date, inflected=False)
    paginate = fpaginate(start, prev, next, next_date, ordering)

    return render_to_response('template_status_best.html',{
                                'status':status_list, # список статусов
                                'all_status_count':all_status_count, # всего авторов
                                'all_user_count':all_user_count, # всего юзеров
                                'all_user':user_list, # список всех юзеров
                                'all_user_count_p':all_user_count_p, # всего опубликованных статусов
                                'current':'best', # название текущей вкладки
                                'yes_votes_list':best_cookies['yes_votes_list'], # лучшие статусы отмеченные юзером
                                'no_votes_list':best_cookies['no_votes_list'], # худшие статусы отмеченные юзером
                                'yes_votes_list_count':best_cookies['yes_votes_list_count'], # количество лучших статусов
                                'paginate':paginate # пейджинатор по датам
                            }, context_instance=RequestContext(request))

