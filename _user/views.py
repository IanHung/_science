# Create your views here.
# Create your views here.

from django.shortcuts import render
from _content.models import StructureNode, get_queryset_descendants, Paragraph, hashTagParser, tagSaveHelper, Image, Timelike, Dataset, datasetFormatter
from _user.forms import ParagraphFormLabbook, ImageFormLabbook, TimelikeFormLabbook, DataFormLabbook, PublishForm, UpdateFormLabbook
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.http import urlquote
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

@login_required
def userDashboard(request):
                        
    top_article_list = get_queryset_descendants(StructureNode.objects.exclude(rating__isnull=True).order_by('-rating__rating').filter(subscribedUser=request.user)).filter(content_type=None).filter(isPublished=True)
    
    
    return render(request, '_home/home2.html', {'top_article_list':top_article_list})


@login_required
def userArticleIndex(request):    
    all_article_list = StructureNode.objects.filter(Q(mptt_level=0)|Q(isUpdate=True)).filter(author=request.user, isPublished=True).exclude(rating__isnull=True).order_by('-pubDate')
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
            
    return render(request, '_user/publishArticleMain.html', {'top_article_list':top_article_list})

@login_required
def userArticleDelete(request):
    if (request.method == 'POST'):
        nodeToDelete = StructureNode.objects.get(id = int(request.POST['nodeID']))
        nodeToDelete.delete()
    return HttpResponseRedirect(reverse('userArticleIndex'))
    
@login_required
def userComment(request):

    comment_list = StructureNode.objects.filter(isPublished = False)
    
    return render(request, '_commentGarden/commentgarden.html', {'comment_list': comment_list,}) #'form':CommentForm()})

@login_required
def userPublish(request):
    labbook_imageNode_list = StructureNode.objects.filter(isLabnote = True, author=request.user, content_type__model='image') #when filtering model must be lower case.
    labbook_timelikeNode_list = StructureNode.objects.filter(isLabnote = True, author=request.user, content_type__model='timelike')
    labbook_dataNode_list = StructureNode.objects.filter(isLabnote = True, author=request.user, content_type__model='dataset')
    publishForm = PublishForm()
    if (request.method == 'POST'):
        print(request.POST)
        publishForm = PublishForm(request.POST)
        if (publishForm.is_valid()):
            experimentNode = StructureNode()
            experimentNode.title = publishForm.cleaned_data['publishFormTitle']
            experimentNode.author = request.user
            experimentNode.isPublished = True
            experimentNode.position = getPositionForRoots()
            experimentNode.save()
            tagList = hashTagParser(publishForm.cleaned_data['publishFormTag'])
            restrictedTagListSave(request, experimentNode, tagList) 
            for sectionNodeIndex in range(0, int(request.POST['numberOfSections'])):
                sectionNode = StructureNode()
                sectionNode.title = request.POST['section_title_'+str(sectionNodeIndex)]
                sectionNode.parent = experimentNode
                sectionNode.author = request.user
                sectionNode.isPublished = True
                sectionNode.position = sectionNodeIndex + 1
                sectionNode.save()
                restrictedTagListSave(request, sectionNode, tagList) 
                for contentNodeIndex in range(0, int(request.POST['numberOfContentSections_'+str(sectionNodeIndex)])):
                    contentNode = StructureNode()
                    contentNode.title = request.POST['section_title_'+str(sectionNodeIndex)] +"_content_"+str(contentNodeIndex)
                    contentNode.parent = sectionNode
                    contentNode.author = request.user
                    contentNode.isPublished = True
                    contentNode.position = contentNodeIndex +1
                    if (request.POST['contentType_section_content_'+str(sectionNodeIndex)+"_"+str(contentNodeIndex)] == "textContent"):
                        tempParagraph = Paragraph()
                        tempParagraph.text = request.POST['text_section_content_'+str(sectionNodeIndex)+"_"+str(contentNodeIndex)]
                        tempParagraph.save()
                        contentNode.content_type = ContentType.objects.get_for_model(Paragraph)
                        contentNode.object_id = tempParagraph.id                        
                        contentNode.save()
                    elif (request.POST['contentType_section_content_'+str(sectionNodeIndex)+"_"+str(contentNodeIndex)] == "imageContent"):
                        contentNode.content_type = ContentType.objects.get_for_model(Image)
                        if (request.POST.get('imageInputLinkSource_section_content_'+str(sectionNodeIndex)+"_"+str(contentNodeIndex))):
                            tempImage = Image()
                            tempImage.linkSource = request.POST['imageInputLinkSource_section_content_'+str(sectionNodeIndex)+"_"+str(contentNodeIndex)]
                            tempImage.save()
                            contentNode.object_id = tempImage.id
                            print("first")
                        elif (request.FILES.get('imageInputLocalSource_section_content_'+str(sectionNodeIndex)+"_"+str(contentNodeIndex))):
                            tempImage = Image()
                            tempImage.localSource = request.FILES['imageInputLocalSource_section_content_'+str(sectionNodeIndex)+"_"+str(contentNodeIndex)]
                            tempImage.save()
                            contentNode.object_id = tempImage.id
                            print("second")
                        elif (request.POST.get('imageInputLabbookSource_section_content_'+str(sectionNodeIndex)+"_"+str(contentNodeIndex))):
                            contentNode.object_id = int(request.POST['imageInputLabbookSource_section_content_'+str(sectionNodeIndex)+"_"+str(contentNodeIndex)])
                            print("third")
                        contentNode.save()
                    elif (request.POST['contentType_section_content_'+str(sectionNodeIndex)+"_"+str(contentNodeIndex)] == "timelikeContent"):
                        contentNode.content_type = ContentType.objects.get_for_model(Timelike)
                        if (request.POST.get('timelikeInputLinkSource_section_content_'+str(sectionNodeIndex)+"_"+str(contentNodeIndex))):
                            tempTimelike = Timelike()
                            tempTimelike.linkSource = request.POST['timelikeInputLinkSource_section_content_'+str(sectionNodeIndex)+"_"+str(contentNodeIndex)]
                            tempTimelike.save()
                            contentNode.object_id = tempTimelike.id
                            print("first")
                        elif (request.FILES.get('timelikeInputLocalSource_section_content_'+str(sectionNodeIndex)+"_"+str(contentNodeIndex))):
                            tempTimelike = Timelike()
                            tempTimelike.localSource = request.FILES['timelikeInputLocalSource_section_content_'+str(sectionNodeIndex)+"_"+str(contentNodeIndex)]
                            tempTimelike.save()
                            contentNode.object_id = tempTimelike.id
                            print("second")
                        elif (request.POST.get('timelikeInputLabbookSource_section_content_'+str(sectionNodeIndex)+"_"+str(contentNodeIndex))):
                            contentNode.object_id = int(request.POST['timelikeInputLabbookSource_section_content_'+str(sectionNodeIndex)+"_"+str(contentNodeIndex)])
                            print("third")
                        contentNode.save()
                    elif (request.POST['contentType_section_content_'+str(sectionNodeIndex)+"_"+str(contentNodeIndex)] == "dataContent"):
                        contentNode.content_type = ContentType.objects.get_for_model(Dataset)
                        if (request.POST.get('dataInputLabbookSource_section_content_'+str(sectionNodeIndex)+"_"+str(contentNodeIndex))):
                            contentNode.object_id = int(request.POST['dataInputLabbookSource_section_content_'+str(sectionNodeIndex)+"_"+str(contentNodeIndex)])
                        contentNode.save()
                    restrictedTagListSave(request, contentNode, tagList) 
                        
    return render(request, '_user/publish.html', {'publishForm':publishForm, 'labbook_imageNode_list': labbook_imageNode_list, 'labbook_timelikeNode_list': labbook_timelikeNode_list, 'labbook_dataNode_list': labbook_dataNode_list, })

@login_required
def userSearchForm(request):
    if (request.method == 'POST'):
        if request.POST.get('search', False):
            tagList = hashTagParser(request.POST['search'].replace("#", "  ").strip())
            subject_url = ""
            for tag in tagList:
                subject_url = subject_url + "#" + urlquote(tag)
            argsSearchForm=[subject_url.replace("#", "  ").strip()]
            return HttpResponseRedirect(reverse('userLabbookTag', args=argsSearchForm))
        else:
            return HttpResponseRedirect(reverse('userLabbook'))


@login_required
def userLabbookTextForm(request, subject_url=None):
    if (request.method == 'POST'):    
        image_form = ImageFormLabbook()
        timelike_form = TimelikeFormLabbook()
        data_form = DataFormLabbook()
        text_form = ParagraphFormLabbook(request.POST)
        update_form = UpdateFormLabbook()
        if textFormLabbookSave(request):
            return HttpResponseRedirect('/user/labbook/')
        else:
            if (subject_url):            
                labbook_list = subjectURLqueryList(request.user,subject_url)
            else:
                labbook_list = StructureNode.objects.filter(isLabnote = True, author=request.user).exclude(content_type = None).order_by('-pubDate')                
            return render(request, '_user/labbook.html', {'labbook_list': labbook_list, 'textForm': text_form, 'imageForm': image_form, 'timelikeForm':timelike_form,'dataForm': data_form, 'subject_url':subject_url, 'updateForm':update_form}) 

@login_required
def userLabbookUpdateForm(request, subject_url=None):
    if (request.method == 'POST'):    
        image_form = ImageFormLabbook()
        timelike_form = TimelikeFormLabbook()
        data_form = DataFormLabbook()
        text_form = ParagraphFormLabbook()
        update_form = UpdateFormLabbook(request.POST)
        if update_form.is_valid():
            changedNode = StructureNode.objects.get(pk=int(request.POST['parentID']))
            changedNode.title = update_form.cleaned_data['updateFormTitle']
            changedNode.tag_set.clear()
            tagList = hashTagParser(update_form.cleaned_data['updateFormTag'])
            restrictedTagListSave(request, changedNode, tagList) 
            return HttpResponseRedirect('/user/labbook/')
        else:
            if (subject_url):
                            
                labbook_list = subjectURLqueryList(request.user,subject_url)
            else:
                labbook_list = StructureNode.objects.filter(isLabnote = True, author=request.user).exclude(content_type = None).order_by('-pubDate')                
            return render(request, '_user/labbook.html', {'labbook_list': labbook_list, 'textForm': text_form, 'imageForm': image_form, 'timelikeForm':timelike_form,'dataForm': data_form, 'subject_url':subject_url, 'updateForm':update_form})             
         
@login_required
def userLabbookImageForm(request, subject_url=None):
    print request.POST
    if (request.method == 'POST'):
        text_form = ParagraphFormLabbook()
        image_form = ImageFormLabbook(request.POST)
        timelike_form = TimelikeFormLabbook()
        data_form = DataFormLabbook()
        update_form = UpdateFormLabbook()
        if imageFormLabbookSave(request):
            return HttpResponseRedirect('/user/labbook/')
        else:
            if (subject_url):            
                labbook_list = subjectURLqueryList(request.user,subject_url)
            else:
                labbook_list = StructureNode.objects.filter(isLabnote = True, author=request.user).exclude(content_type = None).order_by('-pubDate')                
            return render(request, '_user/labbook.html', {'labbook_list': labbook_list, 'textForm': text_form, 'imageForm': image_form, 'timelikeForm':timelike_form,'dataForm': data_form, 'subject_url':subject_url, 'updateForm':update_form}) 
         
@login_required
def userLabbookTimelikeForm(request, subject_url=None):
    if (request.method == 'POST'):
        text_form = ParagraphFormLabbook()
        image_form = ImageFormLabbook()
        timelike_form = TimelikeFormLabbook(request.POST)
        data_form = DataFormLabbook(request)
        update_form = UpdateFormLabbook()
        if timelikeFormLabbookSave(request):
            return HttpResponseRedirect('/user/labbook/')
        else:
            if (subject_url):            
                labbook_list = subjectURLqueryList(request.user,subject_url)
            else:
                labbook_list = StructureNode.objects.filter(isLabnote = True, author=request.user).exclude(content_type = None).order_by('-pubDate')                
            return render(request, '_user/labbook.html', {'labbook_list': labbook_list, 'textForm': text_form, 'imageForm': image_form, 'timelikeForm':timelike_form,'dataForm': data_form, 'subject_url':subject_url, 'updateForm':update_form}) 
         
@login_required
def userLabbookDataForm(request, subject_url=None):
    
    if (request.method == 'POST'):
        print(request.POST)
        text_form = ParagraphFormLabbook()
        image_form = ImageFormLabbook()
        timelike_form = TimelikeFormLabbook()
        data_form = DataFormLabbook(request.POST)
        update_form = UpdateFormLabbook()
        if dataFormLabbookSave(request):
            return HttpResponseRedirect('/user/labbook/')
        else:
            if (subject_url):            
                labbook_list = subjectURLqueryList(request.user,subject_url)
            else:
                labbook_list = StructureNode.objects.filter(isLabnote = True, author=request.user).exclude(content_type = None).order_by('-pubDate')                
            return render(request, '_user/labbook.html', {'labbook_list': labbook_list, 'textForm': text_form, 'imageForm': image_form, 'timelikeForm':timelike_form,'dataForm': data_form, 'subject_url':subject_url, 'updateForm':update_form})      

@login_required
def userLabbook(request, subject_url=None):

    text_form = ParagraphFormLabbook()
    image_form = ImageFormLabbook()
    timelike_form = TimelikeFormLabbook()
    data_form = DataFormLabbook()
    update_form = UpdateFormLabbook()
    print(request.POST)
  
    if (subject_url):            
        labbook_list = subjectURLqueryList(request.user,subject_url)
    else:
        labbook_list = StructureNode.objects.filter(isLabnote = True, author=request.user).exclude(content_type = None).order_by('-pubDate')                
    return render(request, '_user/labbook.html', {'labbook_list': labbook_list, 'textForm': text_form, 'imageForm': image_form, 'timelikeForm':timelike_form,'dataForm': data_form, 'subject_url':subject_url, 'updateForm':update_form}) #'form':CommentForm()})

def userLabbookNameTag(request, user_url, subject_url=None):
    userName = user_url
    user = User.objects.get(username = user_url)
    if (subject_url):            
        labbook_list = subjectURLqueryList(user,subject_url)
    else:
        labbook_list = StructureNode.objects.filter(isLabnote = True, author=user).exclude(content_type = None).order_by('-pubDate')
    return render(request, '_user/labbookUser.html', {'labbook_list': labbook_list, 'userName':userName, 'subject_url':subject_url})      

def textFormLabbookSave(request):
        paragraphFormLabbook = ParagraphFormLabbook(request.POST)
        if (paragraphFormLabbook.is_valid()):
            tempParagraph = Paragraph()
            tempParagraph.text = paragraphFormLabbook.cleaned_data['textFormText'] 
            tempParagraph.save()
            tempStructureNode = StructureNode()
            tempStructureNode.title = paragraphFormLabbook.cleaned_data['textFormTitle']
            tempStructureNode.author = request.user
            tempStructureNode.content_type = ContentType.objects.get_for_model(Paragraph)
            tempStructureNode.object_id = tempParagraph.id
            tempStructureNode.isPublished = False
            tempStructureNode.position = getPositionForRoots()
            tempStructureNode.isComment = False
            tempStructureNode.isLabnote = True
            tempStructureNode.save()
            tagList = hashTagParser(paragraphFormLabbook.cleaned_data['textFormTag'])
            restrictedTagListSave(request, tempStructureNode, tagList)  
            print("something is valid")
            return True
        else:
            print("nothing is ever valid")
            return False
        
def imageFormLabbookSave(request):
        imageFormLabbook = ImageFormLabbook(request.POST, request.FILES)
        if (imageFormLabbook.is_valid()):
            tempImage = Image()
            if (request.POST.get('imageFormLinkSource',False)):
                tempImage.linkSource = imageFormLabbook.cleaned_data['imageFormLinkSource']
            if (request.FILES.get('imageFormLocalSource', False)):
                tempImage.localSource = imageFormLabbook.cleaned_data['imageFormLocalSource']
            tempImage.save()
            tempStructureNode = StructureNode()
            tempStructureNode.title = imageFormLabbook.cleaned_data['imageFormTitle']
            tempStructureNode.author = request.user
            tempStructureNode.content_type = ContentType.objects.get_for_model(Image)
            tempStructureNode.object_id = tempImage.id
            tempStructureNode.isPublished = False
            tempStructureNode.position = getPositionForRoots()
            tempStructureNode.isComment = False
            tempStructureNode.isLabnote = True
            tempStructureNode.save()
            tagList = hashTagParser(imageFormLabbook.cleaned_data['imageFormTag'])
            restrictedTagListSave(request, tempStructureNode, tagList)  
            print("something is valid")
            return True
        else:
            print("nothing is ever valid")
            return False
        
def timelikeFormLabbookSave(request):
        timelikeFormLabbook = TimelikeFormLabbook(request.POST, request.FILES)
        if (timelikeFormLabbook.is_valid()):
            tempTimelike = Timelike()
            if (request.POST.get('timelikeFormLinkSource',False)):
                tempTimelike.linkSource = timelikeFormLabbook.cleaned_data['timelikeFormLinkSource']
            if (request.FILES.get('timelikeFormLocalSource', False)):
                tempTimelike.localSource = timelikeFormLabbook.cleaned_data['timelikeFormLocalSource']
            tempTimelike.save()
            tempStructureNode = StructureNode()
            tempStructureNode.title = timelikeFormLabbook.cleaned_data['timelikeFormTitle']
            tempStructureNode.author = request.user
            tempStructureNode.content_type = ContentType.objects.get_for_model(Timelike)
            tempStructureNode.object_id = tempTimelike.id
            tempStructureNode.isPublished = False
            tempStructureNode.position = getPositionForRoots()
            tempStructureNode.isComment = False
            tempStructureNode.isLabnote = True
            tempStructureNode.save()
            tagList = hashTagParser(timelikeFormLabbook.cleaned_data['timelikeFormTag'])
            restrictedTagListSave(request, tempStructureNode, tagList)   
            print("something is valid")
            return True
        else:
            print("nothing is ever valid")
            return False
        
def dataFormLabbookSave(request):
        dataFormLabbook = DataFormLabbook(request.POST)
        if (dataFormLabbook.is_valid()):
            tempDataset = Dataset()
            tempDataset.data = datasetFormatter(request.POST) 
            tempDataset.save()
            tempStructureNode = StructureNode()
            tempStructureNode.title = dataFormLabbook.cleaned_data['dataFormTitle']
            tempStructureNode.author = request.user
            tempStructureNode.content_type = ContentType.objects.get_for_model(Dataset)
            tempStructureNode.object_id = tempDataset.id
            tempStructureNode.isPublished = False            
            tempStructureNode.position = getPositionForRoots()
            tempStructureNode.isComment = False
            tempStructureNode.isLabnote = True
            tempStructureNode.save()
            tagList = hashTagParser(dataFormLabbook.cleaned_data['dataFormTag'])
            restrictedTagListSave(request, tempStructureNode, tagList) 
            print("something is valid")
            return True
        else:
            print("nothing is ever valid data")
            return False

def restrictedTagListSave(request, node, tagList):
    restrictedList = "_science",
    if not request.user.is_staff:
        tagList = filter(lambda x: not x.startswith(restrictedList), tagList)
    for tag in tagList:
        node.tag_set.add(tagSaveHelper(tag))
    node.save()  
        
def getPositionForRoots():
    if StructureNode.objects.filter(mptt_level=0).exists():
        return StructureNode.objects.filter(mptt_level=0).order_by('-position')[0].position+1
    else:
        return 1
    
def subjectURLqueryList(user,subject_url):
    tagList = hashTagParser(subject_url)
    querySet = StructureNode.objects.filter(isLabnote = True, author=user).exclude(content_type = None).order_by('-pubDate')
    for tag in tagList:
        querySet = querySet.filter(tag__name__iexact=tag)
    return querySet
    