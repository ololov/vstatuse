# -*- coding: utf-8 -*-
#
#       Copyright 2010 Yegor Kowalew <kw@sdesign.com.ua>
#

from django import template
#from post.models import Section, Tag, Post
import pytils
register = template.Library()

#есть две шкалы, одна от 100 до 300 вторая от 2 до 20 Вот как узнать где 5 второй шкалы будет размещаться на первой
#b = 5;
#x1 = 100;
#x2 = 300;
#y1 = 2;
#y2 = 20  вот твои значения, думаю разберешься где что
#a = (b-y1)*(x2-x1)/(y2-y1)+x1

#MIN_FONT_PR = 100 #минимальный размер шрифта в процентах
#MAX_FONT_PR = 300 #минимальный размер шрифта в процентах
#MIN_POST_COL = 1

#def font_size(x1, x2, y1, y2, b):
    #return (b-y1)*(x2-x1)/(y2-y1)+x1
    #return 100

@register.filter(name='date_words')
def date_words(value):
    value = pytils.dt.ru_strftime(u"%d %B %Y года", value, inflected=True)
    return value

@register.filter(name='votes_words')
def votes_words(value):
    word = pytils.numeral.choose_plural(value, (u" раз", u" раза", u" раз"))
    value = str(value) + word
    return value

@register.filter(name='point_to_dash')
def point_to_dash(value):
    return str(value).replace(".", "-")


#@register.inclusion_tag('menu_links.html', takes_context=True)
#def menu_links(context):
    #return {
        #'section_list':Section.objects.all(),
    #}

#@register.inclusion_tag('votes.html', takes_context=True)
#def votes(context, request):
    #if context['post'].id in request.session['votes_list']:
        #print 'есть'
    #else:
        #print 'нету'
    #user_vote_flag = False
    #word = pytils.numeral.choose_plural(context['post'].post_votes, (u" раз", u" раза", u" раз"))
    #votes = str(context['post'].post_votes) + word
    #if user_vote_flag:
        #votes_text = '<span>включая и твой голос</span>'
    #else:
        #votes_text = '<a href="#" id="'+str(context['post'].id)+'">понравилась и мне</a>'
    #return {
        #'votes':votes,
        #'post_id':context['post'].id,
        #'votes_text':votes_text
    #}

#@register.inclusion_tag('tag_links.html', takes_context=True)
#def tag_links(context):
    #tags = Tag.objects.all()
    #e = []
    #MAX_POST_COL = 0
    #for t in tags:
        #posts_in_tag = Post.objects.filter(post_tag__id = t.id)
        #t.tag_count = posts_in_tag.count()
        #e.append(posts_in_tag.count())
        #if MAX_POST_COL < posts_in_tag.count():
            #MAX_POST_COL = posts_in_tag.count()
    #for z in tags:
        #z.font_size = font_size(MIN_FONT_PR, MAX_FONT_PR, MIN_POST_COL, MAX_POST_COL, z.tag_count)
    #return {
        #'tags_list':tags
    #}
