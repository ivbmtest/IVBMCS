from django.shortcuts import render, HttpResponse, redirect,reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage
import logging
from .models import *
from .form import *
from user_portal.models import *

import os
from twilio.rest import Client
from django.core.mail import EmailMultiAlternatives,get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.files.storage import FileSystemStorage
import datetime


@login_required(login_url="/")
def agent(request):
    student_form = AgentForm(request.POST or None, request.FILES or None)
    context = {'form': student_form, 'page_title': 'Add Student'}
    if request.method == 'POST':
        if student_form.is_valid():
            first_name = student_form.cleaned_data.get('first_name')
            last_name = student_form.cleaned_data.get('last_name')
            address = student_form.cleaned_data.get('address')
            email = student_form.cleaned_data.get('email')
            gender = student_form.cleaned_data.get('gender')
            password = student_form.cleaned_data.get('password')
            agent_id = student_form.cleaned_data.get('agent_id')
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            print('----------before try')
            try:
                print('--------entered')
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=3, first_name=first_name, last_name=last_name, profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.agent.agent_id = agent_id
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
        student_form = AgentForm()
    
    model_meta = CustomUser._meta
    field_names = [field.verbose_name for field in model_meta.fields]
    filter_fields=['ID','first name', 'last name', 'active', 'date joined', 
                   'email', 'user type', 'gender', 'profile pic', 'address', 'created at', 'updated at']
    filtered_field_names=[names for names in field_names if names in filter_fields]
    y=CustomUser.objects.filter(user_type=3)
    print("--------------y",filtered_field_names)
    page=Paginator(y,5)
    page_list=request.GET.get('page')
    page=page.get_page(page_list)
    print("--------------y",page_list)
    cou=UserProfile.objects.filter(taken_by__exact='').count()
    for items in y:
        items.user_type = 'staff'
        if items.gender=='M':
            items.gender='Male'
        elif items.gender=='F':
            items.gender = 'Female'
    return render(request,'admin/super_user/agent.html',{'form': student_form,'agent_info':y,'field_names': filtered_field_names,'cou':cou})

#delete agent
def del_agent(request,id):
    currency = CustomUser.objects.filter(pk=id)
    currency.delete()
    return redirect('agent')

def update_agent(request,id):
    if request.method == 'POST':
        agent=CustomUser.objects.get(pk=id)
        agent_form=AgentForm(request.POST,instance=agent)
        if agent_form.is_valid:
            instance = agent_form.save(commit=False)
            # instance.usrid = request.user
            agent.updated_at = datetime.datetime.now()
            instance.save()
            return redirect('agent')
    else:
        id = request.GET['id']
        agent=CustomUser.objects.get(pk=id)
        agent_form = AgentForm(instance=agent)
        agent_form = str(agent_form)
        return JsonResponse({'success': True, 'form':agent_form})

def add_agent(request):
    student_form = AgentForm(request.POST or None, request.FILES or None)
    context = {'form': student_form, 'page_title': 'Add Student'}
    if request.method == 'POST':
        if student_form.is_valid():
            first_name = student_form.cleaned_data.get('first_name')
            last_name = student_form.cleaned_data.get('last_name')
            address = student_form.cleaned_data.get('address')
            email = student_form.cleaned_data.get('email')
            gender = student_form.cleaned_data.get('gender')
            password = student_form.cleaned_data.get('password')
            agent_id = student_form.cleaned_data.get('agent_id')
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=3, first_name=first_name, last_name=last_name, profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.student.course = agent_id
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_student'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")
    return render(request, 'hod_template/add_student_template.html', context)




def age_consulting(request):
    val = request.GET['val']
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        num = request.POST['num']
        serv = request.POST['ser']
        msg = request.POST['msg']
        print("Full set",name,email,num,serv,msg)
       
        service = srvc.objects.get(svname=serv)
        request.session['service_id_data'] = serv

        if CustomUser.objects.filter(email=email,phone_number=num):
            user = CustomUser.objects.get(email=email)
            print("user first---------",user,"enter name --- ",name)
            if user.first_name != name:
                print("That user alredy reg. but name  is not same.")
                return render(request,'Agent/age_consulting.html',{'err':'That user alredy reg. but name  is not same.','value':val})
            elif user_service_details.objects.filter(user_id=user.id,service=service).exists():
                print("that service alredy exists")
                return render(request,'Agent/age_consulting.html',{'err':f'That {val} service alredy applyed','value':val})
            else:
                print("Request Approved")
                
                apply = user_service_details.objects.create(user_id=user, service=service,msg=msg,agent_id=request.user)
                apply.save()
                return render(request,'User/user_dashboard/payment.html')    

        elif CustomUser.objects.filter(email=email).exists():
            print("email alredy")
            return render(request,'Agent/age_consulting.html',{'err':'Email Already Registered','value':val})
        elif CustomUser.objects.filter(phone_number=num).exists():
            print("phone alredy")
            return render(request,'Agent/age_consulting.html',{'err':'phone number  already registered','value':val})
        else:
            #create accout
            print("agent user name :",request.user)
            
            acc = CustomUser.objects.create_user(email=email,phone_number=num,first_name = name,password=email)
            acc.save()
            apply = user_service_details.objects.create(user_id=acc, service=service,msg=msg,agent_id=request.user)
            apply.save()
            
            print("booikng session",service)
        #u = request.session['username']
        #print("cusom user",CustomUser.objects.get(email=request.user.email))
            u = request.user
            service = srvc.objects.get(svname=serv)
            print("booikng session",service)
            return render(request,'User/user_dashboard/payment.html')   
    else:
        return render(request,'Agent/age_consulting.html',{'value':val}) 
        # user_instance,user_created = CustomUser.objects.get_or_create(email=email,defaults={'name':name,'email':email,'phone_number':num })
        # # userdata = user_service_details
        # if userdata.objects.filter(email=u).exists() and userdata.objects.filter(phone_number='').exists():
        #     user_up = userdata.objects.get(email=u)
        #     user_up.name = name
        #     user_up.phone_number = num
        #     user_up.status = 0
        #     user_up.save()
        #     print("new userupdate")
        
        # if not user_created:
        #     print('user already exist with email',user_instance.email) 
        # service_data,service_created = user_service_details.objects.get_or_create(user_id=user_instance,service=service,defaults={'msg':msg},status=1)
        #request.session['user_id_data'] = user_instance.id     
             


def userpro_agent(request):
    userid = request.GET['xid']
    user_info = CustomUser.objects.get(pk=userid)

    if request.method == 'POST':
        ser = request.POST['sel_ser']
        sel_ser = srvc.objects.get(pk=int(ser))
        if user_service_details.objects.filter(user_id=user_info,service=sel_ser):
            return render(request,'Agent/user_pro.html',{'user_info':user_info,'err':1})
        else:
            return render(request,'Agent/age_consulting.html',{'value':sel_ser.svname,'user_info':user_info})  


    return render(request,'Agent/user_pro.html',{'user_info':user_info})





@login_required(login_url="/")
def age_home(request):
    return render(request,'Agent/age_home.html')

@login_required(login_url="/")
def age_service(request):
    ser = user_service_details.objects.filter(agent_id = request.user)
    print(ser)
    return render(request,'Agent/age_services.html',{'my_service':ser})


@login_required(login_url="/")
def age_notify(request):
    return render(request,'Agent/notification.html')



@login_required(login_url="/")
def age_all_service(request):
    return render(request,'Agent/all_service.html')



@login_required(login_url="/")
def age_payments(request):
    return render(request,'Agent/payments.html')


