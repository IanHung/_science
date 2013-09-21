'''
Created on 2013-09-18

@author: Ian
'''
from django.forms import ModelForm
from _content.models import Image, Paragraph, Timelike, StructureNode

class ImageForm(ModelForm):
    class Meta:
        model = Image
        
class ParagraphForm(ModelForm):
    class Meta:
        model = Paragraph
        
class TimelikeForm(ModelForm):
    class Meta:
        model = Timelike
        
class StructureNodeTitleForm(ModelForm):
    class Meta:
        model = StructureNode
        fields =['title']
        