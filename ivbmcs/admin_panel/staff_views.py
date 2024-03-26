from django.shortcuts import render, HttpResponse, redirect,reverse,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage
import logging
from .models import *
from .form import *
from user_portal.models import *
from django.contrib.auth.hashers import check_password

import os
# from twilio.rest import Client
from django.core.mail import EmailMultiAlternatives,get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.files.storage import FileSystemStorage
import datetime


def staff_dashboard(request):
    cou=user_service_details.objects.filter(taken_by__isnull=True).count()
    staff_ord = user_service_details.objects.filter(taken_by=request.user.staff).count()
    print("cou ::: ::",cou)
    my_order_count = user_service_details.objects.filter(user_id=request.user).count()
    
    print(my_order_count)
    model_meta = user_service_details._meta    
    field_names = [field.verbose_name for field in model_meta.fields 
                   if field.verbose_name not in ['Upload Document(.pdf)','Upload Image(.jpg/.jpeg)','Status','Taken']]
    
    latest_record = user_service_details.objects.all().order_by('-created_at')[:5]
    return render(request,'admin/staff/main_layout.html',{'cou':cou,'take':my_order_count,'staff_accept_ord':staff_ord,"latest_data":latest_record,"field_names":field_names})


@login_required(login_url="/")
def staff(request):
    staff_form = StaffForm(request.POST or None, request.FILES or None)
    context = {'form': staff_form, 'page_title': 'Add Staff'}
    if request.method == 'POST':
        if staff_form.is_valid():
            first_name = staff_form.cleaned_data.get('first_name')
            last_name = staff_form.cleaned_data.get('last_name')
            address = staff_form.cleaned_data.get('address')
            email = staff_form.cleaned_data.get('email')
            gender = staff_form.cleaned_data.get('gender')
            password = staff_form.cleaned_data.get('password')
            category = staff_form.cleaned_data.get('category')
            passport = request.FILES['profile_pic']
            print('-------------------',passport)
            print('----------before try')
            try:
                print('--------entered')
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=2, first_name=first_name, last_name=last_name, profile_pic=passport)
                user.gender = gender
                user.address = address
                user.staff.category = category
                user.updated_at = datetime.datetime.now()
                user.is_staff=1
                user.save()
                messages.success(request, "Successfully Added")
                print('-------------exit')
                # return redirect(reverse('add_student'))
            
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")
    else:
        staff_form = StaffForm()
    
    model_meta = CustomUser._meta
    field_names = [field.verbose_name for field in model_meta.fields]
    filter_fields=['ID','first name', 'last name', 'active', 'date joined', 
                   'email', 'user type', 'gender', 'profile pic', 'address', 'created at', 'updated at']
    filtered_field_names=[names for names in field_names if names in filter_fields]
    y=CustomUser.objects.filter(user_type=2)
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
    
    # page=Paginator(y,5)
    # page_list=request.GET.get('page')
    # page=page.get_page(page_list)
    # print("--------------y",page_list)
    # cou=UserProfile.objects.filter(taken_by__isnull=True).count()

    print("s",y)

    for i in y:
        print(i.staff.category)

    staff_cat = ctgry.objects.all()

    for items in y:
        items.user_type = 'staff'
        if items.gender=='M':
            items.gender='Male'
        elif items.gender=='F':
            items.gender = 'Female'
    return render(request, 'admin/super_user/staff.html', {
        'form': staff_form,'staff_info':y,'field_names': filtered_field_names,'staff_cat':staff_cat,
        'start_index': start_index,"page_parameter": page_parameter,
        "paginate_parameter": paginate_parameter})
    # return render(request,'admin/super_user/staff.html',{'form': staff_form,'staff_info':y,'field_names': filtered_field_names,'cou':cou,'staff_cat':staff_cat})

#delete agent
def del_staff(request,id):
    currency = CustomUser.objects.filter(pk=id)
    currency.delete()
    return redirect('staff')

def update_staff(request,id):
    if request.method == 'POST':
        staff=CustomUser.objects.get(pk=id)
        staff_form=StaffForm(request.POST,instance=staff)
        if staff_form.is_valid:
            instance = staff_form.save(commit=False)
            if 'password' in request.POST and request.POST['password']:
                instance.set_password(request.POST['password']) 
            instance.updated_at = datetime.datetime.now()
            instance.save()
            return redirect('staff')
    else:
        id = request.GET['id']
        staff=CustomUser.objects.get(pk=id)
        staff_form = StaffForm(instance=staff)
        staff_form = str(staff_form)
        return JsonResponse({'success': True, 'form':staff_form})



@login_required(login_url="/")
def staff_orders(request):
    model_meta = user_service_details._meta
    field_names = [field.verbose_name for field in model_meta.fields]

    # Retrieve service objects related to the current staff user's category
    sv = srvc.objects.filter(svcategory=request.user.staff.category)
    print("sssv",sv)
    # Retrieve orders related to the filtered services and not yet taken by anyone
    orders = user_service_details.objects.filter(service__in=sv, taken_by__isnull=True)
    paginate_by = request.GET.get('paginate_by',5)
    try:
        paginate_by = int(paginate_by)
    except (ValueError, TypeError):
        # Return an error response if paginate_by cannot be converted to an integer
        return JsonResponse({'success': False, 'error': 'Invalid value for paginate_by'})

    if paginate_by is None:
        page=Paginator(orders,paginate_by)  # paginate_by 5
    else:
        page=Paginator(orders,paginate_by)
    
    page_list=request.GET.get('page')
    page=page.get_page(page_list)
    _request_copy_1 = request.GET.copy()
    _request_copy_2 = request.GET.copy()
    page_parameter = _request_copy_1.pop('page', True) and _request_copy_1.urlencode()
    paginate_parameter = _request_copy_2.pop('paginate_by', True) and _request_copy_2.urlencode()
    start_index = (page.number - 1) * int(paginate_by) + 1
    print('----------start index----------',start_index)
    print('----------paginate_parameter----------',paginate_parameter)
    print('----------page_parameter----------',page_parameter)
    return render(request, 'admin/staff/orders.html', 
                  {'order_info': page, 'field_names': field_names,
                   'start_index': start_index,"page_parameter": page_parameter,
                   "paginate_parameter": paginate_parameter})
    # Paginate the orders
    # paginator = Paginator(orders, 5)
    # page_number = request.GET.get('page')
    # page = paginator.get_page(page_number)
    # print(page)
    # return render(request, 'admin/staff/orders.html', {'order_info': page, 'field_names': field_names})

@login_required(login_url="/")
def send_message(request, id):
    task = user_service_details.objects.get(pk=id)
    print('task::',task)
    user_details = CustomUser.objects.get(pk=task.user_id.id)

    # Assuming YourServiceModel is the correct model for your 'service' field
    service_instance = srvc.objects.get(pk=task.service.svid)

    # Call the function to get the current timestamp
    time = datetime.datetime.now()

    message = request.POST.get('message')
    print('-----message-----', message)
    print('====service======', service_instance)

    # Ensure 'task.service' is passed as 'service' instead of 'task.service.svid'
    user_notification.objects.get_or_create(message=message, timestamp=time,
                                            recepient=user_details, service=service_instance)

    print('-----task-----', task)
    print('====user_details======', user_details.first_name)

    return redirect('task')

def staff_notification(request):
    current_user_id=request.user.id
    notification_details=user_notification.objects.filter(recepient=current_user_id).order_by('-timestamp')
    # for val in notification_details:
    print('--------notifi',notification_details)
    return render(request,'admin/staff/staff_notification.html',{'notification_details':notification_details})


def staff_profile(request):
    return render(request,'admin/staff/staff_profile.html')

def staff_password_reset(request):
    if  request.method == "POST":
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
    return render(request,'admin/staff/change_password.html')

def staff_tickets(request):
    # try:
    print(request.user)
    service_details = user_service_details.objects.filter(taken_by=request.user.staff.id).order_by('-created_at')
    service_instance = user_service_details.objects.filter(taken_by=request.user.staff.id)
    for val in service_instance:
        print('----------service_instance',val.user_id.id)
        user_details = CustomUser.objects.filter(pk=val.user_id.id)
    model_meta = user_service_details._meta
    field_names = [field.verbose_name for field in model_meta.fields]
    filter_fields=['Service', 'Documents', 'agent_id','Payment']
    filtered_field_names=[names for names in field_names if names in filter_fields]
    
    paginate_by = request.GET.get('paginate_by',5)
    try:
        paginate_by = int(paginate_by)
    except (ValueError, TypeError):
        # Return an error response if paginate_by cannot be converted to an integer
        return JsonResponse({'success': False, 'error': 'Invalid value for paginate_by'})

    if paginate_by is None:
        page=Paginator(service_details,paginate_by)  # paginate_by 5
    else:
        page=Paginator(service_details,paginate_by)
    
    page_list=request.GET.get('page')
    page=page.get_page(page_list)
    _request_copy_1 = request.GET.copy()
    _request_copy_2 = request.GET.copy()
    page_parameter = _request_copy_1.pop('page', True) and _request_copy_1.urlencode()
    paginate_parameter = _request_copy_2.pop('paginate_by', True) and _request_copy_2.urlencode()
    start_index = (page.number - 1) * int(paginate_by) + 1
    print('----------start index----------',start_index)
    print('----------paginate_parameter----------',paginate_parameter)
    print('----------page_parameter----------',page_parameter)
    return render(request, 'admin/staff/tickets.html',
                  {
                      'service_details':service_details,'field_names':filtered_field_names,
                      'phone_number':user_details.phone_number,'email':user_details.email,
                      'start_index': start_index,"page_parameter": page_parameter,
                      "paginate_parameter": paginate_parameter})
    
    # return render(request,'admin/staff/tickets.html',{'service_details':service_details,
    #                                                 'field_names':filtered_field_names,
    #                                                 'phone_number':user_details.phone_number,
    #                                                 'email':user_details.email})
    # except:
    #     print('exeptiosn===========')
    #     return render(request,'admin/staff/tickets.html',{'service_details':service_details})
    
    
    
def close_ticket(request,id):
    user_service_details_instance=user_service_details.objects.get(pk=id)
    user_service_details_instance.call_back_request=2
    user_service_details_instance.save()
    return redirect('staff_tickets')

def staff_own_update(request):
    if request.method == 'POST':
        first = request.POST['first']
        last  = request.POST['last']
        email = request.POST['email']
        phone = request.POST['phone']
        user = CustomUser.objects.get(email=request.user.email)
        user.first_name = first
        user.last_name = last
        user.email = email
        user.phone_number = phone
        user.save()
        return render(request,'admin/staff/staff_profile.html')