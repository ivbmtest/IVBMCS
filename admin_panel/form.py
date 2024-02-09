from django import forms
from .models import *
from django.core.exceptions import ValidationError


class crncForm(forms.ModelForm):
    class Meta():
        model = crnc
        fields = "__all__"

class up_crncForm(forms.ModelForm):
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

class DocumentForm(forms.ModelForm):
    class Meta():
        model = DocumentsRequired
        fields = "__all__" 

class Tax_masterForm(forms.ModelForm):
    class Meta():
        model = txmst
        fields = "__all__"     

class TaxdeailsForm(forms.ModelForm):
    class Meta():
        model = txdet
        fields = "__all__"                         
        
class userForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        fields = ['name', 'phone_number', 'email', 'service', 'document', 'image', 'payment']