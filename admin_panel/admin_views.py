from django.shortcuts import render, HttpResponse, redirect,reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage
import logging
from .models import *
from .form import *
from django.contrib import messages
import os
from twilio.rest import Client
from django.core.mail import EmailMultiAlternatives,get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.files.storage import FileSystemStorage
import datetime



def admin(request):
    admin_form = AdminForm(request.POST or None, request.FILES or None)
    context = {'form': admin_form, 'page_title': 'Add Staff'}
    if request.method == 'POST':
        if admin_form.is_valid():
            first_name = admin_form.cleaned_data.get('first_name')
            last_name = admin_form.cleaned_data.get('last_name')
            address = admin_form.cleaned_data.get('address')
            email = admin_form.cleaned_data.get('email')
            gender = admin_form.cleaned_data.get('gender')
            password = admin_form.cleaned_data.get('password')
            passport = request.FILES['profile_pic']
            # fs = FileSystemStorage()
            # filename = fs.save(passport.name, passport)
            # passport_url = fs.url(filename)
            print('----------before try')
            try:
                print('--------entered',admin_form.errors)
                user = CustomUser.objects.create_superuser(
                    email=email, password=password, user_type=1, first_name=first_name, last_name=last_name, profile_pic=passport)
                user.gender = gender
                user.address = address
                user.updated_at = datetime.datetime.now()
                user.save()
                messages.success(request, "Successfully Added")
                print('-------------exit')
                # return redirect(reverse('add_student'))
            
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")
    else:
        admin_form = AdminForm()
    
    model_meta = CustomUser._meta
    field_names = [field.verbose_name for field in model_meta.fields]
    filter_fields=['ID','first name', 'last name', 'active', 'date joined', 
                   'email', 'user type', 'gender', 'profile pic', 'address', 'created at', 'updated at']
    filtered_field_names=[names for names in field_names if names in filter_fields]
    y=CustomUser.objects.filter(user_type=1)
    print("--------------y",filtered_field_names)
    page=Paginator(y,5)
    page_list=request.GET.get('page')
    page=page.get_page(page_list)
    print("--------------y",page_list)
    cou=UserProfile.objects.filter(taken_by__exact='').count()
    return render(request,'admin/super_user/admin.html',{'form': admin_form,'admin_info':y,'field_names': filtered_field_names,'cou':cou})

#delete agent
def del_admin(request,id):
    currency = CustomUser.objects.filter(pk=id)
    currency.delete()
    return redirect('agent')

def update_admin(request,id):
    if request.method == 'POST':
        admin=CustomUser.objects.get(pk=id)
        admin_form=AdminForm(request.POST,instance=admin)
        if admin_form.is_valid:
            instance = admin_form.save(commit=False)
            # instance.usrid = request.user
            instance.updated_at = datetime.datetime.now()
            instance.save()
            return redirect('admin')
    else:
        id = request.GET['id']
        admin=CustomUser.objects.get(pk=id)
        admin_form = AdminForm(instance=admin)
        admin_form = str(admin_form)
        return JsonResponse({'success': True, 'form':admin_form})

# def add_agent(request):
#     student_form = AgentForm(request.POST or None, request.FILES or None)
#     context = {'form': student_form, 'page_title': 'Add Student'}
#     if request.method == 'POST':
#         if student_form.is_valid():
#             first_name = student_form.cleaned_data.get('first_name')
#             last_name = student_form.cleaned_data.get('last_name')
#             address = student_form.cleaned_data.get('address')
#             email = student_form.cleaned_data.get('email')
#             gender = student_form.cleaned_data.get('gender')
#             password = student_form.cleaned_data.get('password')
#             agent_id = student_form.cleaned_data.get('agent_id')
#             passport = request.FILES['profile_pic']
#             fs = FileSystemStorage()
#             filename = fs.save(passport.name, passport)
#             passport_url = fs.url(filename)
#             try:
#                 user = CustomUser.objects.create_user(
#                     email=email, password=password, user_type=3, first_name=first_name, last_name=last_name, profile_pic=passport_url)
#                 user.gender = gender
#                 user.address = address
#                 user.student.course = agent_id
#                 user.save()
#                 messages.success(request, "Successfully Added")
#                 return redirect(reverse('add_student'))
#             except Exception as e:
#                 messages.error(request, "Could Not Add: " + str(e))
#         else:
#             messages.error(request, "Could Not Add: ")
#     return render(request, 'hod_template/add_student_template.html', context)