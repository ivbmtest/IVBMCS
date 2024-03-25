from django.shortcuts import render, HttpResponse, redirect,reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
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

from django.contrib.auth.hashers import check_password


@login_required(login_url="/")
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
    for items in y:
        items.user_type = 'staff'
        if items.gender=='M':
            items.gender='Male'
        elif items.gender=='F':
            items.gender = 'Female'
    return render(request, 'admin/super_user/admin.html', {
        'form': admin_form,'admin_info':y,'field_names': filtered_field_names,
        'start_index': start_index,"page_parameter": page_parameter,
        "paginate_parameter": paginate_parameter})
    # return render(request,'admin/super_user/admin.html',{'form': admin_form,'admin_info':y,'field_names': filtered_field_names,'cou':cou})

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
            if 'password' in request.POST and request.POST['password']:
                instance.set_password(request.POST['password']) 
            instance.updated_at = datetime.datetime.now()
            instance.save()
            return redirect('admin_dashboard')
    else:
        id = request.GET['id']
        admin=CustomUser.objects.get(pk=id)
        admin_form = AdminForm(instance=admin)
        admin_form = str(admin_form)
        return JsonResponse({'success': True, 'form':admin_form})


def admin_profile(request):
    return render(request,'admin/super_user/admin_profile.html')

def admin_password_reset(request):
    if  request.method == "POST":
        print("admin_password")
        old = request.POST['old']
        new = request.POST['newpass']
        re_pass = request.POST['re_pass']
        print("new pass:::",new,"current pass :::",request.user.password)
        if not check_password(old, request.user.password):
            return JsonResponse({'success': False})
            
            
        else:
            
            request.user.set_password(new)
            request.user.save()
            update_session_auth_hash(request, request.user)
            return JsonResponse({'success': True, 'result':"Password Successfully Changed"})
    #return render(request,'admin/staff/change_password.html')


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