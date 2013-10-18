from django.conf.urls import patterns, url

from _news import views

urlpatterns = patterns('',
                       url(r'^tag/(?P<subject_url>[^/]+)/$', views.news, name='newstag'),
                       url(r'^$', views.news, name='news'),
                      )
