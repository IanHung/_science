# Create your views here.
import json
from django.shortcuts import render, HttpResponse
from _content.models import StructureNode, Timelike, Tag, get_queryset_descendants, hashTagParser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from _article.forms import PublishForm

def news(request, subject_url=None):
    all_news_list = StructureNode.objects.filter(mptt_level=0, tag__name__startswith="_science").order_by('-pubDate')
    if subject_url:
        all_news_list = subjectURLFilter(all_news_list, subject_url)
    paginator = Paginator(all_news_list, 5)
    page = request.GET.get('page')
    if request.user.is_authenticated():
        labbook_imageNode_list = StructureNode.objects.filter(isLabnote = True, author=request.user, content_type__model='image') #when filtering model must be lower case.
        labbook_timelikeNode_list = StructureNode.objects.filter(isLabnote = True, author=request.user, content_type__model='timelike')
        labbook_dataNode_list = StructureNode.objects.filter(isLabnote = True, author=request.user, content_type__model='dataset')
    else:
        labbook_imageNode_list = None
        labbook_timelikeNode_list = None
        labbook_dataNode_list = None
    try:
        top_article_list = get_queryset_descendants(paginator.page(page))
        current_article_list = paginator.page(page)
    except PageNotAnInteger:
        top_article_list = get_queryset_descendants(paginator.page(1))
        current_article_list = paginator.page(1)
    except EmptyPage:
        top_article_list = get_queryset_descendants(paginator.page(paginator.num_pages))
        current_article_list = paginator.page(paginator.num_pages)
    
    publishForm = PublishForm()
    return render(request, '_news/news.html', {'nodes':top_article_list, 'current_article_list':current_article_list, 'publishForm':publishForm, 'labbook_imageNode_list': labbook_imageNode_list, 'labbook_timelikeNode_list': labbook_timelikeNode_list, 'labbook_dataNode_list': labbook_dataNode_list, })

def subjectURLFilter(query_set, subject_url):
    tagList = hashTagParser(subject_url)
    querySet = query_set
    for tag in tagList:
        querySet = querySet.filter(tag__name__iexact=tag)
    return querySet
