# -*- coding: utf-8 -*-
#
#       Copyright 2010 Yegor Kowalew <kw@sdesign.com.ua>
#

from django.contrib.sitemaps import Sitemap
from status.models import VStatus#, RandomText, Category

class VSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return VStatus.objects.filter(status_status='p').order_by('-status_date')

    def lastmod(self, obj):
        return obj.status_date
