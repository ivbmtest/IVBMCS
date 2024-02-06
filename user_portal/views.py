from django.shortcuts import render,HttpResponse,redirect
from admin_panel.models import *
from django.urls import reverse
from .models import *
from django.http import JsonResponse
from datetime import datetime
import pyotp
from .utils import *



# Create your views here.
def index(request):
    return render(request,'User/user_layout.html')

def about(request):
    return render(request,'User/about.html')

def service(request):
    category=ctgry.objects.all()
    return render(request,'User/service.html',{'service':service})

def service_detail(request):
    service_name=request.GET['service_name']
    # s=request.GET['category_name']
    print('-------------->>',service_name)
    try:
        cat = srvc.objects.get(svname=service_name)
        similar_category=srvc.objects.filter(svcategory=cat.svcategory)
    except srvc.DoesNotExist:
        cat = None
        similar_category=None

    # return render(request,'User/service.html',{'service':s,"sm":sm})
    return render(request,'User/service_detail.html',{'value':service_name,'similar_category':similar_category})

def contact(request):
    return render(request,'User/contact.html')


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
        user='a'
        if user is not None:
            print("data ===>",user_data)
            global msg
            if check_phone_number(user_data):
                send_otp_number(request,user_data)
                print("Phone number found in data.")
                msg = 'otp send your number'
            if check_email(user_data):
                send_otp_email(request,user_data)
                print("Email address found in data.")
                msg = 'otp send your email'
            request.session['username'] = user_data
            return JsonResponse({'success': True, 'result':msg})
        else:
            return render(request,'login.html',{'err':'not user'})
    else:
        return render(request,'login.html',{'err':err})
    
# otp verify

def otp_ver(request):
    err = None
    if request.method == 'POST':
        otp = int(request.POST['code'])
        print("user enter otp :",type(otp))
        username = request.session['username']
        otp_secret_key = request.session['otp_secret_key']
        validate_otp = request.session['validate_otp']

        print("otp scer :",otp_secret_key,"   validay :",validate_otp)
        if otp_secret_key and validate_otp is not None:
            validate_until = datetime.fromisoformat(validate_otp)
            if validate_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key,interval = 60)
                print("=======totp",totp.verify(otp))
                if totp.verify(otp):
                    #user = get_object_or_404(User,username=username)
                    del request.session['otp_secret_key']
                    del request.session['validate_otp']
                    return JsonResponse({'success': True, 'result':"otp verified",
                                         'template_name': '/user_dashboard'})
                    # return render(request,'admin/main_app/main_layout.html')
                
                else:
                    print('----------->>>>>>invalid otp')
                    return JsonResponse({'success': False, 'result':"Invalid OTP",
                                         'template_name': '/user_dashboard'})
                    # return render(request,'admin/main_app/main_layout.html')
            else:
                del request.session['otp_secret_key']
                del request.session['validate_otp']
                return JsonResponse({'success': False, 'result':"OTP Expired"})    
        else:
            pass    
    else:
        pass    
    return render(request,'otp.html') 
    