from django import forms
from .models import crnc


class crncForm(forms.ModelForm):
    class Meta():
        model = crnc
        fields = "__all__"