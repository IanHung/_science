from django import forms

class PublishForm(forms.Form):
    publishFormTitle = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Title", }))
    publishFormTag = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",}), required=False)