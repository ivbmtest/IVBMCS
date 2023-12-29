from django import forms
from .models import *
from django.core.exceptions import ValidationError

class crncForm(forms.ModelForm):
    class Meta():
        model = crnc
        fields = "__all__"
        
class cntryForm(forms.ModelForm):
    class Meta():
        model = cntry
        fields = "__all__"
        
        
class ctgryForm(forms.ModelForm):
    class Meta():
        model = ctgry
        fields = "__all__" 

class srvcForm(forms.ModelForm):
    class Meta():
        model = srvc
        fields = "__all__"        
 
# class crncForm(forms.ModelForm):
#     class Meta():
#         model = crnc
#         fields = "__all__"                           