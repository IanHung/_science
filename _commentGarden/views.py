# Create your views here.

from django.shortcuts import render
from _content.models import StructureNode, hashTagParser, tagSaveHelper, Image, Timelike, Dataset, datasetFormatter, Paragraph
from _article.forms import PublishForm
from _user.views import restrictedTagListSave
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from _content.forms import ImageForm, ParagraphForm, TimelikeForm, StructureNodeTitleForm
from django.forms import model_to_dict

def commentIndex(request):

    comment_list = StructureNode.objects.filter(isPublished = False)
    
    return render(request, '_commentGarden/commentgarden.html', {'comment_list': comment_list,}) #'form':CommentForm()})

def submitComment(request):
    
    if (request.method == 'POST'):
        print(request.POST)
        publishForm = PublishForm(request.POST)
        if (publishForm.is_valid()):
            tagList = hashTagParser(publishForm.cleaned_data['publishFormTag'])
            commentNode = StructureNode()
            commentNode.title= publishForm.cleaned_data['publishFormTitle']
            commentNode.parent_id = int(request.POST['sectionParent'])
            commentNode.author = request.user
            commentNode.isComment = True
            commentNode.position = getPositionForComments(request)
            commentNode.save()
            commentNode.parent.subscribedUser.add(request.user)
            commentNode.subscribedUser.add(commentNode.parent.author)
            commentNode.subscribedUser.add(commentNode.author)
            commentNode.save()
            restrictedTagListSave(request, commentNode, tagList) 
            for contentNodeIndex in range(0, int(request.POST['numberOfContentSections_'+str(0)])):
                tempContentData = {'title': request.POST['publishFormTitle'] +"_content_"+str(contentNodeIndex)}
                contentDataForm = StructureNodeTitleForm(tempContentData)
                if contentDataForm.is_valid():
                    
                    contentNode = contentDataForm.save(commit=False)
                    
                    contentNode.parent = commentNode
                    contentNode.author = request.user
                    contentNode.isComment = True
                    contentNode.position = contentNodeIndex
                    if (request.POST['contentType_section_content_'+str(0)+"_"+str(contentNodeIndex)] == "textContent"):
                        tempParagraph = Paragraph()
                        tempParagraph.text = request.POST['text_section_content_'+str(0)+"_"+str(contentNodeIndex)]
                        tempParagraphDict = model_to_dict(tempParagraph)
                        paragraphForm = ParagraphForm(tempParagraphDict)
                        if paragraphForm.is_valid():
                            tempParagraph = paragraphForm.save()
                        contentNode.content_type = ContentType.objects.get_for_model(Paragraph)
                        contentNode.object_id = tempParagraph.id                        
                        contentNode.save()
                    elif (request.POST['contentType_section_content_'+str(0)+"_"+str(contentNodeIndex)] == "imageContent"):
                        contentNode.content_type = ContentType.objects.get_for_model(Image)
                        if (request.POST.get('imageInputLinkSource_section_content_'+str(0)+"_"+str(contentNodeIndex))):
                            tempImage = Image()
                            tempImage.linkSource = request.POST['imageInputLinkSource_section_content_'+str(0)+"_"+str(contentNodeIndex)]
                            tempImageDict=model_to_dict(tempImage)
                            imageForm = ImageForm(tempImageDict)
                            if imageForm.is_valid():
                                tempImage = imageForm.save()
                                print("working")
                            else:
                                print("notworking")
                            contentNode.object_id = tempImage.id
                            print("first")
                        elif (request.FILES.get('imageInputLocalSource_section_content_'+str(0)+"_"+str(contentNodeIndex))):
                            tempImage = Image()
                            tempImage.localSource = request.FILES['imageInputLocalSource_section_content_'+str(0)+"_"+str(contentNodeIndex)]
                            tempImage.save()
                            contentNode.object_id = tempImage.id
                            print("second")
                        elif (request.POST.get('imageInputLabbookSource_section_content_'+str(0)+"_"+str(contentNodeIndex))):
                            contentNode.object_id = int(request.POST['imageInputLabbookSource_section_content_'+str(0)+"_"+str(contentNodeIndex)])
                            print("third")
                        contentNode.save()
                    elif (request.POST['contentType_section_content_'+str(0)+"_"+str(contentNodeIndex)] == "timelikeContent"):
                        contentNode.content_type = ContentType.objects.get_for_model(Timelike)
                        if (request.POST.get('timelikeInputLinkSource_section_content_'+str(0)+"_"+str(contentNodeIndex))):
                            tempTimelike = Timelike()
                            tempTimelike.linkSource = request.POST['timelikeInputLinkSource_section_content_'+str(0)+"_"+str(contentNodeIndex)]
                            tempTimelikeDict = model_to_dict(tempTimelike)
                            timelikeForm = TimelikeForm(tempTimelikeDict)
                            if timelikeForm.is_valid():
                                tempTimelike = timelikeForm.save()
                            contentNode.object_id = tempTimelike.id
                            print("first")
                        elif (request.FILES.get('timelikeInputLocalSource_section_content_'+str(0)+"_"+str(contentNodeIndex))):
                            tempTimelike = Timelike()
                            tempTimelike.localSource = request.FILES['timelikeInputLocalSource_section_content_'+str(0)+"_"+str(contentNodeIndex)]
                            tempTimelike.save()
                            contentNode.object_id = tempTimelike.id
                            print("second")
                        elif (request.POST.get('timelikeInputLabbookSource_section_content_'+str(0)+"_"+str(contentNodeIndex))):
                            contentNode.object_id = int(request.POST['timelikeInputLabbookSource_section_content_'+str(0)+"_"+str(contentNodeIndex)])
                            print("third")
                        contentNode.save()
                    elif (request.POST['contentType_section_content_'+str(0)+"_"+str(contentNodeIndex)] == "dataContent"):
                        contentNode.content_type = ContentType.objects.get_for_model(Dataset)
                        if (request.POST.get('dataInputLabbookSource_section_content_'+str(0)+"_"+str(contentNodeIndex))):
                            contentNode.object_id = int(request.POST['dataInputLabbookSource_section_content_'+str(0)+"_"+str(contentNodeIndex)])
                        contentNode.save()
                    restrictedTagListSave(request, contentNode, tagList) 
            
    return HttpResponseRedirect(request.POST['prevPage'])


def getPositionForComments(request):
    if StructureNode.objects.filter(parent__id=int(request.POST['sectionParent'])).exists():
        return StructureNode.objects.filter(parent__id=int(request.POST['sectionParent'])).order_by('-position')[0].position+1
    else:
        return 1