# myapp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class Currency_form(forms.ModelForm):
    #email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = crnc
        fields = "__all__"


class Country_form(forms.ModelForm):
    #email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = cntry
        fields = "__all__"
        widgets = {
            'cndescription': forms.Textarea(attrs={'cols': 80, 'rows': 20, 'style': 'width: 100%;height:45px;'}),
        }



class Category_form(forms.ModelForm):
    #email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = ctgry
        fields = "__all__"
        widgets = {
            'cndescription': forms.Textarea(attrs={'cols': 80, 'rows': 20, 'style': 'width: 100%;height:45px;'}),
        }


class Document_form(forms.ModelForm):
    #email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = ctgry
        fields = "__all__"
        widgets = {
            'cndescription': forms.Textarea(attrs={'cols': 80, 'rows': 20, 'style': 'width: 100%;height:45px;'}),
        }

class Service_form(forms.ModelForm):
    #email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = srvc
        fields = "__all__"
        