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
from user_portal.models import *

import os
from twilio.rest import Client
from django.core.mail import EmailMultiAlternatives,get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.files.storage import FileSystemStorage
import datetime
from django.contrib.auth.hashers import check_password
  

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
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=3, first_name=first_name, last_name=last_name, profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.agent.agent_id = agent_id
                user.updated_at = datetime.datetime.now()
                user.save()
                messages.success(request, "Successfully Added")
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
    # cou=UserProfile.objects.filter(taken_by__exact='').count()
    for items in y:
        items.user_type = 'staff'
        if items.gender=='M':
            items.gender='Male'
        elif items.gender=='F':
            items.gender = 'Female'
    
    return render(request, 'admin/super_user/agent.html', {
        'form': student_form,'agent_info':y,'field_names': filtered_field_names,
        'start_index': start_index,"page_parameter": page_parameter,
        "paginate_parameter": paginate_parameter})
    # return render(request,'admin/super_user/agent.html',{'form': student_form,'agent_info':y,'field_names': filtered_field_names,'cou':cou})

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
            if 'password' in request.POST and request.POST['password']:
                instance.set_password(request.POST['password']) 
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




def user_consulting_by_agent(request):
    val = request.GET['val']
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        num = request.POST['num']
        serv = request.POST['ser']
        msg = request.POST['msg']
       
        service = srvc.objects.get(svname=serv)
        request.session['service_id_data'] = serv

        if CustomUser.objects.filter(email=email,phone_number=num):
            user = CustomUser.objects.get(email=email)
            if user.first_name != name:
                return render(request,'Agent/age_consulting.html',{'err':'That user alredy reg. but name  is not same.','value':val})
            elif user_service_details.objects.filter(user_id=user.id,service=service).exists():
                return render(request,'Agent/age_consulting.html',{'err':f'That {val} service alredy applyed','value':val})
            else:               
                apply = user_service_details.objects.create(user_id=user, service=service,msg=msg,agent_id=request.user)
                apply.save()
                return render(request,'User/user_dashboard/payment.html')    

        elif CustomUser.objects.filter(email=email).exists():
            return render(request,'Agent/age_consulting.html',{'err':'Email Already Registered','value':val})
        elif CustomUser.objects.filter(phone_number=num).exists():
            return render(request,'Agent/age_consulting.html',{'err':'phone number  already registered','value':val})
        else:
            #create accout           
            acc = CustomUser.objects.create_user(email=email,phone_number=num,first_name = name,password=email,user_type=4)
            acc.save()
            apply = user_service_details.objects.create(user_id=acc, service=service,msg=msg,agent_id=request.user)
            apply.save()
            u = request.user
            service = srvc.objects.get(svname=serv)
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
    s = user_service_details.objects.all()
    tot_ord = user_service_details.objects.filter()
    li = [i.created_at.month for i in s if i.user_id.user_type == "4"]

    d = {i: li.count(i) if i in li else 0 for i in range(1, 13)}
    mon_base_ord = [d[i] for i in range(1, 13)]
    
    return render(request,'Agent/age_home.html',{'mon_base_ord':mon_base_ord})

@login_required(login_url="/")
def age_service(request):
    ser = user_service_details.objects.filter(agent_id = request.user)
    return render(request,'Agent/age_services.html',{'my_service':ser})

@login_required(login_url="/")
def agent_profile(request):
    return render(request,'Agent/agent_profile.html')

@login_required(login_url="/")
def age_notify(request):
    return render(request,'Agent/notification.html')



@login_required(login_url="/")
def age_all_service(request):
    return render(request,'Agent/all_service.html')



@login_required(login_url="/")
def age_payments(request):
    agent_payment_details = user_service_details.objects.filter(agent_id=request.user.id)
    for val in agent_payment_details:
        print(val.payment)
    return render(request,'Agent/payments.html',{'agent_payment_details':agent_payment_details})


def age_details(request):
    return render(request, 'Agent/age_details.html')


def agent_password_reset(request):
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
    #return render(request,'admin/staff/change_password.html')
    
    
def agent_registration(request):
    if request.method == 'POST':
        a=False
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        user_photo = request.FILES.get('user_photo')
        address = request.POST.get('address')
        adhaar = request.FILES.get('adhaar')
        pancard = request.FILES.get('pancard')
        gst = request.FILES.get('gst')
        license = request.FILES.get('license')

        # Check if user with the given email already exists
        existing_user = CustomUser.objects.filter(email=email).first()
        if existing_user:
            print('-------------existing user ----->>>')
            # User already exists, handle accordingly (e.g., show error message)
            return redirect('error_page')  # Redirect to an error page or handle appropriately

        # Create a new user
        user = CustomUser.objects.create_user(
            email=email, password='', user_type=3, first_name=first_name,
            last_name=last_name, profile_pic=user_photo, phone_number=phone_number)
        user.gender = ''
        user.address = address
        user.updated_at = datetime.datetime.now()
        user.save()

        # Retrieve the associated Agent object
        agent = Agent.objects.get(admin=user.id)
        print('--------agent>>',agent)
        print('--------agentid >>',agent.id)
        # Check if agent exists
        if agent is None:
            # Handle the case where agent does not exist
            # Redirect or show error message as needed
            return redirect('error_page')  # Redirect to an error page or handle appropriately

        # Create associated Individual entry
        IndividualAgent.objects.create(individual_agent = agent,agent_photo=user_photo, aadhar=adhaar,
                                  pancard=pancard, gst_certificate=gst, license=license)

        # Redirect to a success page or next step
        a=True
        return render(request, 'Agent/age_details.html',{'popup':a})
    else:
        return render(request, 'agent_registration.html')
    
def company_registration(request):
    if request.method == 'POST':
        com_name = request.POST['company_name']
        com_number = request.POST['com_number']
        com_email = request.POST['com_email']
        tin_num = request.POST['tin_num']
        address = request.POST['com_address']
        pin = request.POST['com_pincode']
        com_acc_name = request.POST['com_acc_name']
        com_acc_number = request.POST['com_acc_number']
        com_ifsc_code = request.POST['com_ifsc_number']
        
        com_gst=request.FILES.get("com_gst")
        in_corporate = request.FILES.get('in_corporate')
        art_associate = request.FILES.get('art_associate')
        com_pancard = request.FILES.get('com_pan')

        com_dir_name = request.POST['com_dir_name']
        com_dir_postion = request.POST['com_dir_postion']
        com_dir_number = request.POST['com_dir_number']
        com_dir_email = request.POST['com_dir_email']
        
        dir_image = request.FILES.get('dir_image')
        dir_adhar = request.FILES.get('dir_adhar')
        dir_pancard = request.FILES.get('dir_pan')
        print("work")
        a=False
        if CustomUser.objects.filter(email=com_email).exists():
            return render(request,'Agent/age_details.html',{'msg_com':'Company Email already exists'})
            
        elif CustomUser.objects.filter(phone_number=com_number).exists():
            return render(request,'Agent/age_details.html',{'msg_com':'Company phone number already exists'})

        elif com_directors.objects.filter(director_email=com_dir_email).exists():
            return render(request,'Agent/age_details.html',{'msg_dir':'Company director Email already exists'})
        
        elif com_directors.objects.filter(director_phone_number=com_dir_number).exists():
            return render(request,'Agent/age_details.html',{'msg_dir':'Company director phonenumber already exists'})
        
        else:
            
            new_comp = CustomUser.objects.create_user(email=com_email,phone_number=com_number,first_name=com_name,user_type=3)
            new_comp.save()
            print("new - comp",new_comp.agent.id)
            age = Agent.objects.get(id=new_comp.agent.id)
            print("age",age)
            company_details = Company_details.objects.create(agents=age,tin_num=tin_num,com_address=address,pincode=pin,company_gst=com_gst,
                                                     incorporation_certificate=in_corporate,article_of_association=art_associate,
                                                      company_pancard=com_pancard)
            company_details.save()
           
            
            bank_acc = bank_accound_details.objects.create(company_name=new_comp,acc_holder_name=com_acc_name,acc_number=com_acc_number,
                                                           ifsc_code=com_ifsc_code)
            bank_acc.save()
            com_dir = com_directors.objects.create(company=company_details, director_name=com_dir_name, director_postion=com_dir_postion,
                                                    director_email=com_dir_email,director_phone_number=com_dir_number,director_img=dir_image,
                                                    director_adhar=dir_adhar,director_pancard=dir_pancard)
            com_dir.save()
            # send notification
            
            a=True
            return render(request, 'Agent/age_details.html',{'popup':a})
