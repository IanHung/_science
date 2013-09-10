from django import forms

class ParagraphFormLabbook(forms.Form):
    textFormTitle = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Title", }))
    textFormText = forms.CharField(widget=forms.Textarea(attrs={"row": 5,}))
    textFormTag = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",}), required=False)
        
class ImageFormLabbook(forms.Form):
    imageFormTitle = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Title", }))
    imageFormTag = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",}), required=False)
    imageFormLocalSource = forms.ImageField(required=False)
    imageFormLinkSource = forms.URLField(widget=forms.TextInput(attrs={"placeholder": "Enter URL of image."}),required=False)
    
    def clean(self):
        cleaned_data = super(ImageFormLabbook, self).clean()
        
        if not ((not 'imageFormLocalSource' in self.files) ^ (not cleaned_data.get("imageFormLinkSource"))):
            print("this is the point of failure")
            raise forms.ValidationError("Please submit exactly one source")
        
        return cleaned_data
        
class TimelikeFormLabbook(forms.Form):
    timelikeFormTitle = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Title", "accept": "video/*",}))
    timelikeFormTag = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",}), required=False)
    timelikeFormLocalSource = forms.FileField(required=False)
    timelikeFormLinkSource = forms.URLField(widget=forms.TextInput(attrs={"placeholder": "Enter URL of video."}),required=False)
        
    def clean(self):
        cleaned_data = super(TimelikeFormLabbook, self).clean()
        
        if not ((not cleaned_data.get("timelikeFormLocalSource")) ^ (not cleaned_data.get("timelikeFormLinkSource"))):
            print("this is the point of failure")
            raise forms.ValidationError("Please submit exactly one source")
        
        return cleaned_data
    
class DataFormLabbook(forms.Form):
    dataFormTitle = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Title", }))
    dataFormTag = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",}), required=False)
    
class PublishForm(forms.Form):
    publishFormTitle = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Title", }))
    publishFormTag = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",}), required=False)
    
class UpdateFormLabbook(forms.Form):
    updateFormTitle = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Title", }))
    updateFormTag = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",}), required=False)