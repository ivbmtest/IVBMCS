from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from admin_panel.models import *
from .models import *
from .utils import *
from .common_functions import *

from django.http import JsonResponse

from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

def user_login(request):
    return render(request,'User/user_dashboard/main_layout.html')


@csrf_exempt
def user_dash_home(request):
    
    try:
        user_last = user_service_details.objects.filter(user_id=request.user.id).order_by('-created_at')[0]
        recom = srvc.objects.filter(svcategory = user_last.service.svcategory)
    except:
        recom = srvc.objects.all()
        print("if >>  ::::: ::: ::")
    if request.method == 'POST':
        first = request.POST['first']
        last = request.POST['last']
        number = request.POST['number']
        email = request.POST['email']
        print(first,last,email,number)
        print("ph ::::::;",request.user.phone_number)
        if request.POST['pre_email'] != request.user.email:
            if CustomUser.objects.filter(email=email):
                return JsonResponse({'success': False, 'err':"email already exists"})
        elif CustomUser.objects.filter(phone_number=number):
            return JsonResponse({'success': False, 'err':"Phone number already exists"})

        else:
            user = CustomUser.objects.get(id=request.user.id)
            user.first_name=first
            user.last_name=last
            user.email=email
            user.phone_number=number
            user.save()
            print(user.first_name)
            return JsonResponse({'success': True,'template_name': '/user_home'})
    
    else:

        return render(request,'User/user_dashboard/user_home.html',{'recommended':recom})
    


def my_service(request):
    #current_user = request.session['username']
    
    current_user = request.user
    print("user services  ->",user_service_details.objects.all())
    print("service : : 25 :::",current_user.id)
    #current_user = get_user_details(current_user) 
    my_ser = user_service_details.objects.filter(user_id=current_user.id)
    print(current_user.email)
    user_det = authenticate(request, email=current_user.email)
    print(user_det)

    return render(request,'User/user_dashboard/my_service.html',{'my_service':my_ser,})


def user_notify(request):
    # notification_data = user_notification.objects.all()
    # print('======== ========',request.session['username'])
    user_detail=get_object_or_404(CustomUser, last_name=request.user.last_name)
    
    print("user_notify",user_detail.email)
    
    service_details =  user_service_details.objects.filter(user_id=user_detail)
    user_notifications = user_notification.objects.filter(recepient=user_detail).order_by('-timestamp')
    # notification_detail = 
    print("----- ------",user_notifications)
    for val in service_details:
        print("------ -----",val.service)
    service_details={'notification_details':user_notifications}
    return render(request,'User/user_dashboard/notification.html')

def all_service(request):
    return render(request,'User/user_dashboard/all_service.html')

def payments(request):
    return render(request,'User/user_dashboard/payments.html')

def appointment(request):
    return render(request,'User/consultation.html')


def select_service(request,value=''):
    #current_user =request.session['username']
    current_user = request.user

    print("session stroe : ",current_user)
    # try:
    #     print("ok test data",current_user.phone_number)        
    #     #details={'name':current_user.name,'email':current_user.email,'phone':current_user.phone_number}
    #     print("phone :: :: ::",current_user.name)

    #     return render(request,'User/user_dashboard/consultation.html')
    # except:
    #     print("except : ")
    return render(request,'User/user_dashboard/consultation.html',{'value':value})
    

def booking(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        num = request.POST['num']
        serv = request.POST['ser']
        msg = request.POST['msg']
        print(name,email,num,serv,msg)
        #u = request.session['username']
        print("cusom user",CustomUser.objects.get(email=request.user.email))
        u = request.user
        service = srvc.objects.get(svname=serv)
        print("booikng session",service)
        user_instance,user_created = CustomUser.objects.get_or_create(email=email,defaults={'name':name,'email':email,'phone_number':num })
        # userdata = user_service_details
        if userdata.objects.filter(email=u).exists() and userdata.objects.filter(phone_number='').exists():
            user_up = userdata.objects.get(email=u)
            user_up.name = name
            user_up.phone_number = num
            user_up.status = 0
            user_up.save()
            print("new userupdate")
        
        if not user_created:
            print('user already exist with email',user_instance.email) 
        service_data,service_created = user_service_details.objects.get_or_create(user_id=user_instance,service=service,defaults={'msg':msg},status=1)
        request.session['user_id_data'] = user_instance.id
        request.session['service_id_data'] = serv
        
        return render(request,'User/user_dashboard/payment.html')    
    else:
        return render(request,'User/user_dashboard/booking.html')
    
    
def payment(request):
    if request.method == 'POST':
        pay = request.POST.get('pay')
        #current_user = request.session['username']
        current_user = request.user
        #current_user_id = get_user_details(current_user)
        latest_service_details_id=user_service_details.objects.latest('id')
        service_details_id = latest_service_details_id.id
        instance = user_service_details.objects.get(pk = service_details_id)
        if pay == 'on':
            instance.payment=True
        else:
            instance.payment=False    
        instance.save()
        # print("pay val : ",pay)
        if pay:
            serv = request.session.get('service_id_data', None)
            service = srvc.objects.get(svname=serv)
            d = DocumentsRequired.objects.filter( Service = service.svid)
            return render(request,'User/user_dashboard/docu_upload.html',{'form':d,'head':serv})
        else:
            return  HttpResponse('<center><h1 style="color:red">Payment Failed</h1></center>')
    else:
        redirect('payment')

def upload_doc(request):
    if request.method == 'POST':
        received_data = request.session.get('user_id_data', None)
        ser_type = request.POST['ser_type']
        # print("type :::: ",ser_type)
        userid = request.POST['userid']
        # print("userid :::",userid)
        serid = srvc.objects.get(svname=ser_type)
        ser_count = DocumentsRequired.objects.filter(Service=serid)
        # print("type count :::: ",ser_count)
        """user_id = userdata.objects.get(id=userid)
        for i in ser_count:
            f1 = request.FILES[i.DocumentName]
            u = docu_all.objects.create(user=user_id,docu_file=f1)
            u.save()"""
            
        documents = {}
        for document_name, uploaded_file in request.FILES.items():
            documents[document_name] = uploaded_file.name
      
        latest_service_details_id=user_service_details.objects.latest('id')
        service_details_id = latest_service_details_id.id
        instance = user_service_details.objects.get(pk = service_details_id)
        instance.documents=documents
        instance.save()
        # messages.success(request,"File uploaded successfully")
        # return redirect('upload_doc')
        return HttpResponse("Files uploaded successfully.")
    
    else:
        # messages.error(request,"Failed to upload the file")
        # return redirect('upload_doc')
        return HttpResponse("Failed to upload file.")
        # return render(request, 'your_template.html')
    # return HttpResponse(f"Key: {key}, Value: {value} received successfully.")
    # return HttpResponse('<center><h1>Thankyou</h1></center>')