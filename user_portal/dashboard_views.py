from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from admin_panel.models import *
from .models import *
from .utils import *
from .common_functions import *

from django.contrib.auth import authenticate, login, logout


def user_login(request):
    return render(request,'User/user_dashboard/main_layout.html')



def my_service(request):
    current_user = request.session['username']
    current_user = get_user_details(current_user) 
    my_ser = user_service_details.objects.filter(user_id=current_user.id)
    print(current_user.email)
    user_det = authenticate(request, email=current_user.email)
    print(user_det)

    return render(request,'User/user_dashboard/my_service.html',{'my_service':my_ser,})

  

def notification(request):
    # notification_data = user_notification.objects.all()
    print('=================',request.session['username'])
    user_detail=get_object_or_404(userdata, email=request.session['username'])
    service_details =  user_service_details.objects.filter(user_id=user_detail)
    user_notifications = user_notification.objects.filter(recepient=user_detail).order_by('-timestamp')
    # notification_detail = 
    print("------------",user_notifications)
    for val in service_details:
        print("------------",val.service)
    service_details={'notification_details':user_notifications}
    return render(request,'User/user_dashboard/notification.html',service_details)

def all_service(request):
    return render(request,'User/user_dashboard/all_service.html')

def payments(request):
    return render(request,'User/user_dashboard/payments.html')

def appointment(request):
    return render(request,'User/consultation.html')


def select_service(request,value=''):
    current_user =request.session['username']

    print("session stroe : ",current_user)
    try:
        current_user = get_user_details(current_user)
        print("ok test data",current_user)        
        details={'name':current_user.name,'email':current_user.email,'phone':current_user.phone_number}
        print("phone :: :: ::",current_user.name)
        if details:
            return render(request,'User/consultation.html',{'value':value,'details':details})
    except:
        return render(request,'User/consultation.html',{'value':value})
    

def booking(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        num = request.POST['num']
        serv = request.POST['ser']
        msg = request.POST['msg']
        print(name,email,num,serv,msg)
        u = request.session['username']
        service = srvc.objects.get(svname=serv)
        print("booikng session",service)
        user_instance,user_created = userdata.objects.get_or_create(email=email,defaults={'name':name,'email':email,'phone_number':num })
     
        if userdata.objects.filter(email=u).exists() and userdata.objects.filter(phone_number='').exists():
            user_up = userdata.objects.get(email=u)
            user_up.name = name
            user_up.phone_number = num
            user_up.status = 0
            user_up.save()
            print("new userupdate")
        
        if not user_created:
            print('user already exist with email',user_instance.email) 
        service_data,service_created = user_service_details.objects.get_or_create(user_id=user_instance,service=service,defaults={'msg':msg})
        request.session['user_id_data'] = user_instance.id
        request.session['service_id_data'] = serv
        
        return render(request,'User/user_dashboard/payment.html')    
    else:
        return render(request,'User/user_dashboard/booking.html')
    
    
def payment(request):
    if request.method == 'POST':
        pay = request.POST.get('pay')
        current_user = request.session['username']
        current_user_id = get_user_details(current_user)
        latest_service_details_id=user_service_details.objects.latest('id')
        service_details_id = latest_service_details_id.id
        instance = user_service_details.objects.get(pk = service_details_id)
        if pay=='on':
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