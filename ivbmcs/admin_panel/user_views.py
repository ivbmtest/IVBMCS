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


@login_required(login_url="/")
def normal_user(request):
    user_form = UserForm(request.POST or None, request.FILES or None)
    context = {'form': user_form, 'page_title': 'Add User'}
    if request.method == 'POST':
        if user_form.is_valid():
            first_name = user_form.cleaned_data.get('first_name')
            last_name = user_form.cleaned_data.get('last_name')
            address = user_form.cleaned_data.get('address')
            email = user_form.cleaned_data.get('email')
            gender = user_form.cleaned_data.get('gender')
            password = user_form.cleaned_data.get('password')
            # category = user_form.cleaned_data.get('category')
            passport = request.FILES['profile_pic']
            print('-------------------',passport)
            # fs = FileSystemStorage()
            # filename = fs.save(passport.name, passport)
            # passport_url = fs.url(filename)
            print('----------before try')
            try:
                print('--------entered')
                normal_user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=4, first_name=first_name, last_name=last_name, profile_pic=passport)
                normal_user.gender = gender
                normal_user.address = address
                normal_user.updated_at = datetime.datetime.now()
                normal_user.is_staff=0
                normal_user.save()
                messages.success(request, "Successfully Added")
                print('-------------exit')
                
            
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")
    else:
        user_form = UserForm()
    
    model_meta = CustomUser._meta
    field_names = [field.verbose_name for field in model_meta.fields]
    filter_fields=['ID','first name', 'last name', 'active', 'date joined', 
                   'email', 'user type', 'gender', 'profile pic', 'address', 'created at', 'updated at']
    filtered_field_names=[names for names in field_names if names in filter_fields]
    y=CustomUser.objects.filter(user_type=4)
    paginate_by = request.GET.get('paginate_by',5)
    try:
        paginate_by = int(paginate_by)
    except (ValueError, TypeError):
        # Return an error response if paginate_by cannot be converted to an integer
        return JsonResponse({'success': False, 'error': 'Invalid value for paginate_by'})

    if paginate_by is None:
        page=Paginator(y,paginate_by)  # paginate_by 5
    else:
        page=Paginator(y,paginate_by)
    
    page_list=request.GET.get('page')
    page=page.get_page(page_list)
    _request_copy_1 = request.GET.copy()
    _request_copy_2 = request.GET.copy()
    page_parameter = _request_copy_1.pop('page', True) and _request_copy_1.urlencode()
    paginate_parameter = _request_copy_2.pop('paginate_by', True) and _request_copy_2.urlencode()
    start_index = (page.number - 1) * int(paginate_by) + 1
    # print("--------------y",filtered_field_names)
    # page=Paginator(y,5)
    # page_list=request.GET.get('page')
    # page=page.get_page(page_list)
    # print("--------------y",page_list)
    # cou=UserProfile.objects.filter(taken_by__exact='').count()
    for items in y:
        items.user_type = 'staff'
        if items.gender=='M':
            items.gender='Male'
        elif items.gender=='F':
            items.gender = 'Female'
            
    return render(request, 'admin/super_user/normal_user.html', {
        'form': user_form,'staff_info':y,'field_names': filtered_field_names,
        'start_index': start_index,"page_parameter": page_parameter,
        "paginate_parameter": paginate_parameter})
    # return render(request,'admin/super_user/normal_user.html',{'form': user_form,'staff_info':y,'field_names': filtered_field_names,'cou':cou})

#delete agent
def del_user(request,id):
    normal_user = CustomUser.objects.filter(pk=id)
    normal_user.delete()
    return redirect('user')

def update_user(request,id):
    if request.method == 'POST':
        normal_user=CustomUser.objects.get(pk=id)
        user_form=UserForm(request.POST,instance=normal_user)
        if user_form.is_valid:
            instance = user_form.save(commit=False)
            # instance.usrid = request.user
            instance.updated_at = datetime.datetime.now()
            instance.save()
            return redirect('user')
    else:
        id = request.GET['id']
        normal_user=CustomUser.objects.get(pk=id)
        user_form = UserForm(instance=normal_user)
        user_form = str(user_form)
        return JsonResponse({'success': True, 'form':user_form})

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