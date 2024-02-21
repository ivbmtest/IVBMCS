from django import forms
from .models import *
from django.core.exceptions import ValidationError

class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class CustomUserForm(FormSettings):
    email = forms.EmailField(required=True)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    address = forms.CharField(widget=forms.Textarea)
    password = forms.CharField(widget=forms.PasswordInput)
    widget = {
        'password': forms.PasswordInput(),
    }
    profile_pic = forms.ImageField(required=False)

    # def __init__(self, *args, **kwargs):
    #     super(CustomUserForm, self).__init__(*args, **kwargs)

    #     if kwargs.get('instance'):
    #         instance = kwargs.get('instance').admin.__dict__
    #         self.fields['password'].required = False
    #         for field in CustomUserForm.Meta.fields:
    #             self.fields[field].initial = instance.get(field)
    #         if self.instance.pk is not None:
    #             self.fields['password'].widget.attrs['placeholder'] = "Fill this only if you wish to update password"

    # def clean_email(self, *args, **kwargs):
    #     formEmail = self.cleaned_data['email'].lower()
    #     if self.instance.pk is None:  # Insert
    #         if CustomUser.objects.filter(email=formEmail).exists():
    #             raise forms.ValidationError(
    #                 "The given email is already registered")
    #     else:  # Update
    #         dbEmail = self.Meta.model.objects.get(
    #             id=self.instance.pk).admin.email.lower()
    #         if dbEmail != formEmail:  # There has been changes
    #             if CustomUser.objects.filter(email=formEmail).exists():
    #                 raise forms.ValidationError("The given email is already registered")

    #     return formEmail

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'gender',  'password','profile_pic', 'address' ]


class AgentForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AgentForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Agent
        fields = CustomUserForm.Meta.fields + \
            ['agent_id']


class AdminForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Admin
        fields = CustomUserForm.Meta.fields


class StaffForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = CustomUserForm.Meta.fields + \
            ['category' ]

class UserForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Users
        fields = CustomUserForm.Meta.fields
        
class crncForm(forms.ModelForm):
    class Meta():
        model = crnc
        # fields = ['crname', 'crsymbol', 'crdescription', 'crstatus',  'usrid' ]
        fields = "__all__"

# class up_crncForm(forms.ModelForm):
#     class Meta():
#         model = crnc
#         fields = "__all__"
       
class cntryForm(forms.ModelForm):
    class Meta():
        model = cntry
        fields = "__all__"

#state form
class stateForm(forms.ModelForm):
    class Meta():
        model = states
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

#format
       
class Format_Form(forms.ModelForm):
    class Meta():
        model = formt
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