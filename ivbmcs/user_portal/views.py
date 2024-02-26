from django.shortcuts import render,HttpResponse,redirect
from admin_panel.models import *
from django.urls import reverse
from .models import *
from django.http import JsonResponse
from datetime import datetime
from .utils import *

from .common_functions import *
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    return render(request,'User/user_layout.html')

def about(request):
    return render(request,'User/about.html')

def service(request):
    return render(request,'User/service.html')

def contact(request):
    return render(request,'User/contact.html')

def service_details(request):
    s=request.GET['s']
    #cat = srvc.objects.get(svname=s)
    try:
        cat = srvc.objects.get(svname=s)
        sm=srvc.objects.filter(svcategory=cat.svcategory)
    except srvc.DoesNotExist:
        cat = None
        sm=None
    return render(request,'User/service_details.html',{'service':s,"sm":sm})

def consulting(request):
    return render(request,'User/free_consulting.html')


def initial_consult(request,value=''):
    if request.method == 'POST':
        # input_value = request.POST.get('my_input')
        phone_number=request.POST.get('phone_number')
        Free_consult_detail.objects.create(phone_number=phone_number,service=value)
        return render(request,'User/home.html')


# otp request form 

def login_otp(request):
    err = None
    if request.method == 'POST':
        user_data = request.POST['user']
        print('-------------user_data------>>>>>>>>>>>>>>',user_data)
        request.session['user_data'] = user_data
        global msg
        if check_phone_number(user_data):
            send_otp_number(request,user_data)
            print("Phone number found in data.")
            msg = 'otp send your number'
            user_name = user_data

            request.session['user_last_name'] = user_name+"@ivbm"
        if check_email(user_data):
            send_otp_email(request,user_data)
            print("Email address found in data.")
            msg = 'otp send your email'
            user_name =  user_data.split('@')[0]

            request.session['user_last_name'] = user_name+"@ivbm"
        print("email user name : ",user_name)

        return JsonResponse({'success': True, 'result':msg})
    else:
        return render(request,'login.html',{'err':err})

# def otp_ver(request):
#     err = None
#     if request.method == 'POST':
#         otp = request.POST['code']
#         print("user enter otp :",otp)
#         user_name = request.session['username']
#         # otp_secret_key = request.session['otp_secret_key']
#         validate_otp = request.session['validate_otp']
#         val_otp = request.session['otp']
#         validate_until = datetime.fromisoformat(validate_otp)
#         if validate_until > datetime.now():
#             if otp == val_otp:
                
#                 if CustomUser.objects.filter(username=user_name).exists() and User.objects.filter(email=request.session['user_data']).exists():
#                     print("User alredy exits ")
#                     user = User.objects.get(username = user_name)
#                     user.set_password(val_otp)
#                     user.save()
#                     del request.session['username']
#                     del request.session['otp']
#                     del request.session['validate_otp'] 
#                 else:
#                     print("new user")
#                     if '@' in request.session['user_data']:
#                         user = CustomUser.objects.create_user(username = user_name,password=val_otp,email=request.session['user_data'])
#                     else:
#                         user = CustomUser.objects.create_user(username = user_name,password=val_otp)
#                     user.save()
#                     del request.session['username']
#                     del request.session['otp']
#                     del request.session['validate_otp']
#                 login(request,user)
                   
#                 return JsonResponse({'success': True, 'result':"otp verified",'template_name': '/user_home'})
#             else:
#                 print('----------->>>>>>invalid otp')
#                 return JsonResponse({'success': False, 'result':"Invalid OTP"})
#         else:
#             # del request.session['otp_secret_key']
#             del request.session['validate_otp']
#             return JsonResponse({'success': False, 'result':"OTP Expired"})   
#     else:
#         pass    
#     return render(request,'otp.html') 
        
# otp verify

def otp_ver(request):
    err = None
    if request.method == 'POST':
        otp = request.POST['code']
        print("user enter otp :",otp)
        user_name = request.session['user_data']
        print('---------------user_data',request.session['user_data'])
        print('---------------user_last_name',request.session['user_last_name'])
        # otp_secret_key = request.session['otp_secret_key']
        validate_otp = request.session['validate_otp']
        val_otp = request.session['otp']
        validate_until = datetime.fromisoformat(validate_otp)
        if validate_until > datetime.now(): 
            if otp != val_otp:
                
                if CustomUser.objects.filter(email=request.session['user_data']).exists() or CustomUser.objects.filter(phone_number=request.session['user_data']).exists():
                    print("User alredy exits ")
                    check = get_user_details(request.session['user_data'])
                    print("check",check.id)
                    user = CustomUser.objects.get(id = check.id)
                    u =  authenticate(request, email=user_name, password=user.password)
                    print("user_name ::: 137 ",u)
                    user.set_password(val_otp)
                    user.save()
                    
                    print("login",user.email)
                    
                    del request.session['otp']
                    del request.session['validate_otp'] 
                else:
                    print("new user")
                    if '@' in request.session['user_data']:
                        user = CustomUser.objects.create_user(email=request.session['user_data'],password=val_otp,user_type=4,last_name=request.session['user_last_name'])
                    else:
                        user = CustomUser.objects.create_user(email=request.session['user_last_name'],phone_number=request.session['user_data'],password=val_otp,user_type=4,last_name=request.session['user_last_name'])
                    user.save()
                   
                    del request.session['otp']
                    del request.session['validate_otp']
                
                login(request, user,backend='django.contrib.auth.backends.ModelBackend')   
                return JsonResponse({'success': True, 'result':"otp verified",'template_name': '/user_home'})
            else:
                print('----------->>>>>>invalid otp')
                return JsonResponse({'success': False, 'result':"Invalid OTP"})
        else:
            # del request.session['otp_secret_key']
            del request.session['validate_otp']
            return JsonResponse({'success': False, 'result':"OTP Expired"}) 
        # if otp_secret_key and validate_otp is not None:
        #     validate_until = datetime.fromisoformat(validate_otp)
        #     if validate_until > datetime.now():
        #         totp = pyotp.TOTP(otp_secret_key,interval = 60)
        #         print("=======totp",totp.verify(otp))
        #         if totp.verify(otp):
        #             #user = get_object_or_404(User,username=username)
        #             del request.session['otp_secret_key']
        #             del request.session['validate_otp']

        #             if userdata.objects.filter(email=username).exists() or userdata.objects.filter(phone_number=username):
        #                 print("user alredy exits ")
        #                 pass
        #             else:
        #                 print("new user")
        #                 try:
        #                     new = userdata(email=username)
        #                 except:
        #                     new = userdata(phone_number = username)
        #                 new.save()
        #                 request.session['username'] = new.id
        #             return JsonResponse({'success': True, 'result':"otp verified",'template_name': '/user_dashboard'})
        #             # return render(request,'admin/main_app/main_layout.html')
        #         else:
        #             print('----------->>>>>>invalid otp')
        #             return JsonResponse({'success': False, 'result':"Invalid OTP"})
        #             # return render(request,'admin/main_app/main_layout.html')
        #     else:
        #         del request.session['otp_secret_key']
        #         del request.session['validate_otp']
        #         return JsonResponse({'success': False, 'result':"OTP Expired"})    
        # else:
        #     pass    
    else:
        pass    
    return render(request,'otp.html') 
    