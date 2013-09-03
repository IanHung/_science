# Create your views here.
import json
from django.shortcuts import render, HttpResponse
from _content.models import StructureNode, Timelike
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q


def home(request):
    all_article_list = StructureNode.objects.filter(Q(mptt_level=0)|Q(isUpdate=True)).exclude(rating__isnull=True).order_by('-rating__rating')
    paginator = Paginator(all_article_list, 25) # Show 25 contacts per page
    
    page = request.GET.get('page')
    try:
        top_article_list = paginator.page(page)        
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        top_article_list = paginator.page(1)
        page = "1"
    
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        top_article_list = paginator.page(paginator.num_pages)
        page = paginator.num_pages
        
    if page == "1":
        return render(request, '_home/home.html', {'top_article_list':top_article_list})
    else:
        return render(request, '_home/home2.html', {'top_article_list':top_article_list})         
    

def getSubject(request, subject_url):
    try:
        top_article_list = StructureNode.objects.filter(Q(mptt_level=0)|Q(isUpdate=True)).exclude(rating__isnull=True).order_by('-rating__rating').filter(tag__name__iexact=subject_url)
    except StructureNode.DoesNotExist:
        raise Http404
    
    return render(request, '_home/home.html', {'top_article_list':top_article_list})

