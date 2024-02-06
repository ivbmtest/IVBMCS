from django.shortcuts import render,HttpResponse,redirect
from admin_panel.models import *
from django.urls import reverse
from django.contrib import messages
from .models import *
from django.http import JsonResponse
from datetime import datetime
import pyotp
from .utils import *
from .common_functions import *




def user_login(request):
    return render(request,'User/user_dashboard/main_layout.html')

def my_service(request):
    return render(request,'User/user_dashboard/my_service.html')
    
def notification(request):
    return render(request,'User/user_dashboard/notification.html')

def all_service(request):
    return render(request,'User/user_dashboard/all_service.html')

def payments(request):
    return render(request,'User/user_dashboard/payments.html')

def appointment(request):
    return render(request,'User/consultation.html')

def select_service(request,value=''):
    current_user =request.session['username']
    try:
        current_user = get_user_details(current_user)        
        details={'name':current_user.name,'email':current_user.email,'phone':current_user.phone_number}
        
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
        service = srvc.objects.get(svname=serv)
        
        user_instance,user_created = userdata.objects.get_or_create(email=email,
                                                                    defaults={
                                                                        'name':name,'email':email,'phone_number':num
                                                                        })
        if not user_created:
            print('user already exist with email',user_instance.email)
            
        service_data,service_created = user_service_details.objects.get_or_create(user_id=user_instance,
                                                                                  service=service,
                                                                                  defaults={'msg':msg})
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
        return HttpResponse("Failed to upload files.")
        # return render(request, 'your_template.html')
    # return HttpResponse(f"Key: {key}, Value: {value} received successfully.")
    # return HttpResponse('<center><h1>Thankyou</h1></center>')