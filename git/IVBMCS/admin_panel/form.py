from django import forms
from .models import *


class crncForm(forms.ModelForm):
    class Meta():
        model = crnc
        #crname =forms.CharField(label='tw', widget=forms.TextInput(attrs={'id': 'cr_id'}))
        fields = "__all__"
        
class CountryForm(forms.ModelForm):
    class Meta():
        model = cntry
        fields = "__all__"

class CategoryForm(forms.ModelForm):
    class Meta():
        model = ctgry
        fields = "__all__" 

class ServiceForm(forms.ModelForm):
    class Meta():
        model = srvc
        fields = "__all__"
 
 
# class crncForm(forms.ModelForm):
#     class Meta():
#         model = crnc
#         fields = "__all__"                           