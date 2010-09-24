# -*- coding: utf-8 -*-
#
#       Copyright 2010 Yegor Kowalew <kw@sdesign.com.ua>
#

from django.db.models import Count
from django.shortcuts import HttpResponse, render_to_response, HttpResponseRedirect
from status.models import VStatus, RandomText, Category
from customuser.models import CustomUser
from django.core.paginator import Paginator
from django.template.context import RequestContext
from dateutil.relativedelta import *
import pytils, time, re, datetime

def not_zero(status_id_zero):
    '''Убираю нолики с статус id'''
    b = r'^0+(?P<n>\d+)$'
    return re.sub(b, '\g<n>', str(status_id_zero))

def user_best_cookies(request):
    '''Выбираю куки пользователя'''
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

def def_values(request):
    '''Значения используемые в большинстве вьюшек'''
    best_cookies = user_best_cookies(request)
    all_user = CustomUser.objects.annotate(num_status=Count('vstatus')).order_by('-num_status')
    try:
        random_header = RandomText.objects.order_by('?')[1].random_text_body
    except:
        random_header = ''
    return {
            'random_header': random_header,
            'all_status_count':VStatus.objects.all().count(),
            'all_user_count':all_user.count(),
            'all_user':all_user[:5],
            'all_user_count_p':VStatus.objects.filter(status_status='p').count(),
            'yes_votes_list':best_cookies['yes_votes_list'],
            'no_votes_list':best_cookies['no_votes_list'],
            'yes_votes_list_count':best_cookies['yes_votes_list_count'],
            'category': Category.objects.all()#Category.objects.annotate(num_status=Count('vstatus')).filter(num_status__gt = 0).order_by('-num_status')
        }

def category_description(category_id=False):
    """ Выборка для Category descripton  """
    category_for_desc = ''
    if category_id:
        category_for_desc = Category.objects.get(id = category_id)
    else:
        for i in Category.objects.all():
            category_for_desc = category_for_desc + i.category_name + ' '
    try:
        return category_for_desc.encode("UTF-8")
    except:
        return ''

def index(request, error_message=None, message_type=None):
    '''Стартовая страница'''
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
    dict = {'status':status,
            'current':'sort',
            'title':'по Рейтингу',
            'message':error_message,
            'message_type':message_type,
            'description': 'Cтатусы для вконтакте ' + category_description()
        }
    dict2 = def_values(request).copy()
    dict2.update(dict)
    return render_to_response('template_status.html', dict2, context_instance=RequestContext(request))

def by_this_date(request, this_date):
    '''По конкретной дате'''
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
    dict = {'status':status,
            'current':'sort',
            'title':pytils.dt.ru_strftime(u"за %d %B %Y", datetime.datetime.fromtimestamp(time.mktime(time.strptime(this_date, "%Y-%m-%d"))), inflected=True),
            'description': 'Cтатусы для вконтакте отсортированные по дате ' + category_description(),
    }
    dict2 = def_values(request).copy()
    dict2.update(dict)
    return render_to_response('template_status.html', dict2, context_instance=RequestContext(request))

def this_status(request, id):
    '''Просмотр статуса'''
    dict = {'st':VStatus.objects.get(id=not_zero(id)),
            'title':'Статус #'+id.encode("UTF-8"),
        }
    dict2 = def_values(request).copy()
    dict2.update(dict)
    return render_to_response('template_this_status.html', dict2, context_instance=RequestContext(request))

def random_ten(request):
    '''Случайная десятка'''
    dict = {'status':VStatus.objects.order_by('?')[:10],
            'current':'sort',
            'title':'Случайная десятка',
            'description': 'Случайная десятка статусов для вконтакте ' + category_description(),
        }
    dict2 = def_values(request).copy()
    dict2.update(dict)
    return render_to_response('template_status_ten.html', dict2, context_instance=RequestContext(request))

def by_this_rating(request, rating):
    '''По конкретному рейтингу'''
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
    dict = {'status':status,
            'current':'sort',
            'title':'по рейтингу равному '+rating.replace("-", ".").encode("UTF-8"),
            'description': 'Статусы с рейтингом ' + rating.replace("-", ".").encode("UTF-8") + ' ' + category_description(),
        }
    dict2 = def_values(request).copy()
    dict2.update(dict)
    return render_to_response('template_status.html', dict2, context_instance=RequestContext(request))

def by_autor_rating(request, rating):
    '''По рейтингу автора'''
    status_list = CustomUser.objects.filter(user_rating=rating.replace("-", "."))
    paginator = Paginator(status_list, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        status = paginator.page(page)
    except (EmptyPage, InvalidPage):
        status = paginator.page(paginator.num_pages)

    dict = {'status':status,
            'current':'sort',
            'title':'по рейтингу равному '+rating.replace("-", ".").encode("UTF-8"),
            'description': 'Просмотр авторов с рейтингом '+rating.replace("-", ".").encode("UTF-8"),
        }
    dict2 = def_values(request).copy()
    dict2.update(dict)
    return render_to_response('template_autors.html', dict2, context_instance=RequestContext(request))

def order(request, ordering):
    '''Первый пункт меню "Сортировка" '''
    order_list = [['date','по Дате','-status_date'], ['rating','по Рейтингу','-status_rating'], ['user-top','по Понравившимся','-status_rating']]
    for i in order_list:
        if i[0] == ordering:
            ordering = i
            this_url = i[0]
    best_cookies = user_best_cookies(request)
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

    dict = {'status':status,
            'title':ordering[1],
            'current':'sort',
            'description': 'Просмотр статусов для вконтакте, отсортированных ' + ordering[1]
        }
    dict2 = def_values(request).copy()
    dict2.update(dict)
    return render_to_response('template_status.html', dict2, context_instance=RequestContext(request))

def by_autor(request, autor):
    '''По автору'''
    status_list = VStatus.objects.filter(status_status='p', status_author__id=autor).order_by('-status_rating')
    this_user = CustomUser.objects.get(id = autor)
    paginator = Paginator(status_list, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        status = paginator.page(page)
    except (EmptyPage, InvalidPage):
        status = paginator.page(paginator.num_pages)
    dict = {'status':status,
            'title':'Автор ' + this_user.first_name.encode("UTF-8") + ', статусов ' + str(status_list.count()),
            'current':'autor',
            'description': 'Просмотр статусов для вконтакте автора: ' + this_user.first_name.encode("UTF-8")
                            +' '+ this_user.last_name.encode("UTF-8")
                            +', Статусов:' + str(status_list.count()),
        }
    dict2 = def_values(request).copy()
    dict2.update(dict)
    return render_to_response('template_status.html', dict2, context_instance=RequestContext(request))

def autor_yes_no(request, autor, yesno):
    '''По автору, с положительными или отрицательными голосами'''
    if yesno == 'yes-votes':
        status_list = VStatus.objects.filter(status_status='p', status_author__id=autor, status_vote_yes__gt = 0).order_by('-status_rating')
    elif yesno == 'no-votes':
        status_list = VStatus.objects.filter(status_status='p', status_author__id=autor, status_vote_no__gt = 0).order_by('-status_rating')
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    user = CustomUser.objects.get(id = autor).username
    paginator = Paginator(status_list, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        status = paginator.page(page)
    except (EmptyPage, InvalidPage):
        status = paginator.page(paginator.num_pages)
    dict = {'status':status,
            'title':'Автор ' + this_username.encode("UTF-8") + ', статусов ' + str(status_list.count()),
            'current':'autor',
            'description': 'Cтатусы для вконтакте, Автор: '
                            + user.first_name.encode("UTF-8")
                            + ' ' + user.last_name.encode("UTF-8")
                            + ', статусов ' + str(status_list.count()),
        }
    dict2 = def_values(request).copy()
    dict2.update(dict)
    return render_to_response('template_status.html', dict2, context_instance=RequestContext(request))

def by_category(request, category):
    '''По категории'''
    category = Category.objects.get(category_slug = category)
    status_list = VStatus.objects.filter(status_status='p', status_category = category).order_by('-status_rating')
    paginator = Paginator(status_list, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        status = paginator.page(page)
    except (EmptyPage, InvalidPage):
        status = paginator.page(paginator.num_pages)
    dict = {'status':status,
            'title':category.category_name.encode("UTF-8"),
            'current':'category',
            'description': 'Cтатусы для вконтакте, '
                            + category.category_name.encode("UTF-8") + ' '
                            + category_description(category.id),
        }
    dict2 = def_values(request).copy()
    dict2.update(dict)
    return render_to_response('template_status.html', dict2, context_instance=RequestContext(request))

def all_autor(request):
    '''Все авторы'''
    user_list = CustomUser.objects.all()
    paginator = Paginator(user_list, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        status = paginator.page(page)
    except (EmptyPage, InvalidPage):
        status = paginator.page(paginator.num_pages)
    dict = {'status':status,
            'title':'Все пользователи',
            'current':'autor',
            'description': 'Авторов: '+ str(user_list.count()),
        }
    dict2 = def_values(request).copy()
    dict2.update(dict)
    return render_to_response('template_autors.html', dict2, context_instance=RequestContext(request))

def add_status(request):
    '''Добавление статуса'''
    from django.contrib.auth.models import User
    from django.core.context_processors import csrf
    from status.forms import *
    c = {}
    c.update(csrf(request))
    if request.method == 'POST': # If the form has been submitted...
        form = AddStatusForm(request.POST)
        if form.is_valid():
            if request.user.is_superuser:
                nn_user = CustomUser.objects.get(id = request.user.id)
            else:
                nn_user = CustomUser.objects.filter(is_superuser=True).order_by('?')[0]
            new_status = form.save(commit=False)
            new_status.status_author = nn_user
            new_status.status_date = datetime.datetime.today()
            new_status.status_status = 'd'
            new_status.save()
            form.save_m2m()
        else:
            dict = {'title':'Добавление статуса',
                'form': form,
                'description': 'Страница добавления нового статуса для вконтакте',
                }
            dict2 = def_values(request).copy()
            dict2.update(dict)
            return render_to_response('template_add_status.html', dict2)

        return HttpResponseRedirect('/add-status') # Все отлично, редирект на предыдущую

    else:
        form = AddStatusForm().as_p()

    dict = {'title':'Добавление статуса',
            'form': form,
            'description': 'Страница добавления нового статуса для вконтакте',
        }
    dict2 = def_values(request).copy()
    dict2.update(dict)
    return render_to_response('template_add_status.html', dict2, context_instance=RequestContext(request))

def vote(request, action, id):
    '''Голосование'''
    def_val = def_values(request)
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
        this_status.status_rating = round(((this_status.status_vote_yes+this_status.status_vote_no)*100.)/def_val['all_user_count_p'], 2)
        this_status.status_vote_yes_date = datetime.datetime.now()
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
        this_status.status_rating = round(((this_status.status_vote_yes+this_status.status_vote_no)*100.)/def_val['all_user_count_p'], 2)
        this_status.save()
    return HttpResponse('')

def order_best(request, ordering, num):
    '''Лучшие за день, неделю, месяц'''
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
    start_day = datetime.date.today()
    num = int(num)
    if ordering == 'day':
        date_start = start_day - relativedelta(days=num)
        #print date_start
        status_list = VStatus.objects.filter(status_status='p', status_vote_yes_date__month=date_start.month, status_vote_yes_date__year=date_start.year, status_vote_yes_date__day=date_start.day).order_by('-status_rating')[:10]
        #print status_list
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

    dict = {'status':status_list,
            'current':'best',
            'paginate':paginate,
        }
    dict2 = def_values(request).copy()
    dict2.update(dict)
    return render_to_response('template_status_best.html', dict2, context_instance=RequestContext(request))
