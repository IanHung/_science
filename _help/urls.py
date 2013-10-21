from django.conf.urls import patterns, url

from _article import views

urlpatterns = patterns('',
                       url(r'^article/(?P<article_url>[^/]+)/$', views.getArticle, name='helparticle'),
                      )
