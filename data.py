'''
Created on 2013-06-17

@author: Ian Hung
'''
from _content.models import StructureNode, Rating, ViewCount, Paragraph, Image, Timelike
import random
from django.contrib.contenttypes.models import ContentType


def GetObjectType(typeID):
    if(typeID==1):
        return ContentType.objects.get_for_model(Timelike)
    elif(typeID==2):
        return ContentType.objects.get_for_model(Image)
    elif(typeID==3):
        return ContentType.objects.get_for_model(Paragraph)

def DataTest(s, h, publish, words):
    numberOfExperiments = random.randint(s, h)
    print(numberOfExperiments)
    for x in range(1, numberOfExperiments+1):
        print(x)
        tempExp = StructureNode(title=words + "experiment" + str(x), slug=words + "experiment" + str(x),  isPublished=publish, position=x)
        tempExp.save()
        numberOfArticles = random.randint(1, 5)
        for y in range(1, numberOfArticles+1):
            tempArt = StructureNode(title= words + "experiment" + str(x)+"Article" + str(y), slug="article" + str(y), parent_id=tempExp.id, isPublished=publish, position=y)
            tempArt.save()
            tempArt.rating.rating = random.randint(1,50)
            tempArt.rating.save()
            numberOfSubparts = random.randint(1,10)
            for z in range(1, numberOfSubparts+1):
                tempContent = StructureNode(title=words + "experiment" + str(x)+"Article" + str(y)+"Content" + str(z), slug="content" + str(z), parent_id=tempArt.id, content_type=GetObjectType(random.randint(1,3)), object_id = 1, isPublished=publish, position=z)
                tempContent.save()

#DataTest(5,5, True, "test3")

def DataTestWithComments(h, words):
    numberOfExperiments = random.randint(1, h)
    print(numberOfExperiments)
    for x in range(1, numberOfExperiments+1):
        
        tempExp = StructureNode(title=words + "experiment" + str(x), slug=words + "experiment" + str(x),  isPublished=True, position=x)
        tempExp.save()
        numberOfArticles = random.randint(1, 5)
        for y in range(1, numberOfArticles+1):
            
            tempArt = StructureNode(title= words + "experiment" + str(x)+"Article" + str(y), parent_id=tempExp.id, isPublished=True, position=y)
            tempArt.save()
            tempArt.rating.rating = random.randint(1,50)
            tempArt.rating.save()
            numberOfSubparts = random.randint(1,10)
            for z in range(1, numberOfSubparts+1):
                
                tempContent = StructureNode(title=words + "experiment" + str(x)+"Article" + str(y)+"Content" + str(z), parent_id=tempArt.id, content_type=GetObjectType(random.randint(1,3)), object_id = 1, isPublished=True, position=z)
                tempContent.save()
                numberofComments = random.randint(1,5)
                for w in range(1, numberofComments+1):
                    tempComment = StructureNode(title=words + "experiment" + str(x) + "Article" + str(y) + "Content" + str(z) + "Comment" + str(w), parent_id=tempContent.id, isPublished=False, position=w)
                    tempComment.save()
                    for xx in range(1, numberofComments+1):
                        print("xx=" + str(xx))
                        tempCommentContent = StructureNode(title=words + "experiment" + str(x) + "Article" + str(y) + "Content" + str(z) + "Comment" + str(w) +"Content" + str(xx), parent_id=tempComment.id, content_type=GetObjectType(3), object_id = 1, isPublished=False, position=xx)
                        tempCommentContent.save()

# Need to add another feature to allow for multiple threads of comments and multiple responses to those comments.

#DataTest(10, True, "test10")
DataTestWithComments(5, "commenttest1")


