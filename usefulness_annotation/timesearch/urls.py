from django.conf.urls import patterns, include, url
from django.contrib import admin
from anno.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'timesearch.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^admin/', include(admin.site.urls)),
    (r'^login/$', login),
    (r'^training/(\d{10})/(\d{1,2})/$', training),
    (r'^tasks/(\d{10})/(\d{1,2})/$', tasks),
    (r'^tasks/finished/(\d{10})/(\d{1,2})/$', tasks_finished),
    (r'^search/(\d{10})/(\d{1,2})/(.*?)/$', search),
    (r'^resultsnumber/(\d{10})/(\d{1,2})/(.*?)/$', resultsnumber),
    (r'^annotation/(\d{10})/(\d{1,2})/(.*?)/(.*?)/$', annotation),
    (r'^taskreview/(\d{10})/(\d{1,2})/(.*?)/$', taskreview),
    (r'^LogOutcome/$', log_outcome),
    (r'^LogUrl/$', log_url),
    (r'^LogSatisfaction/$', log_satisfaction),
    (r'^LogRealism/$', log_realism),
    (r'^LogUsefulness/$', log_usefulness),
    (r'^index/$', index),
)
