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
        
        
    # def clean(self):
    #     cleaned_data = super().clean()
    #     cc_myself = cleaned_data.get("svcode")
    #     subject = cleaned_data.get("svname")

    #     if cc_myself and subject:
    #         # Only do something if both fields are valid so far.
    #         # if "help" not in subject:
    #         raise ValidationError(
    #             "Did not send for 'help' in the subject despite " "CC'ing yourself."
    #         )
 
# class crncForm(forms.ModelForm):
#     class Meta():
#         model = crnc
#         fields = "__all__"                           