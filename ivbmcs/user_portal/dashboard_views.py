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


def user_profile(request):
    return render(request,'User/user_dashboard/user_profile.html')

@csrf_exempt
def user_dash_home(request):    
    try:
        user_last = user_service_details.objects.filter(user_id=request.user.id).order_by('-created_at')[0]
        recom = srvc.objects.filter(svcategory = user_last.service.svcategory)
    except:
        recom = srvc.objects.all()
    if request.method == 'POST':
        first = request.POST['first']
        last = request.POST['last']
        number = request.POST['number']
        email = request.POST['email']
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
        all_servie_by_user = user_service_details.objects.filter(user_id=request.user)
        print(all_servie_by_user)
        tot_spend=0
        for i in all_servie_by_user:
            print(i.service.svrate)
            tot_spend =  tot_spend+i.service.svrate
        print(tot_spend)
        
        return render(request,'User/user_dashboard/user_home.html',{'recommended':recom,'tot_spend':tot_spend})
    


def my_service(request): 
    
    current_user = request.user
    my_ser = user_service_details.objects.filter(user_id=current_user.id)
    user_det = authenticate(request, email=current_user.email)
    return render(request,'User/user_dashboard/my_service.html',{'my_service':my_ser,})


def user_notify(request):
    current_user = request.user
    user_detail=get_object_or_404(CustomUser, email=request.user.email)   
    service_details =  user_service_details.objects.filter(user_id=user_detail.id)
    user_notifications = user_notification.objects.filter(recepient=user_detail.id).order_by('-timestamp')
    user_notifications_instance = user_notification.objects.filter(recepient=user_detail.id)
    sender=user_notifications_instance.sender
    service=user_notifications_instance.service
    service_details={'service':service}
    return render(request,'User/user_dashboard/notification.html',
                  {'notification_details':user_notifications,'sender':sender,'service':service})
    
def notification_detail(request,id):
    service_detail=srvc.objects.filter(svname=id)
    user_service_detail= user_service_details.objects.get(service=service_detail[0].svid, user_id=request.user.id)
    user_notification_instance= user_notification.objects.get(service=service_detail[0].svid, recepient=request.user.id)
    user_notification_instance.is_viewed =1
    user_notification_instance.save()
    return render(request,'User/user_dashboard/notification_detail.html',{'user_service_detail':user_service_detail})


def callback_request(request):  
    staff_name=request.POST.get('staff_name')
    print('---------',staff_name)
    sender=request.user
    service=request.POST.get('service')
    message=request.POST.get('message')
    timestamp = datetime.now()
    user_details = CustomUser.objects.get(first_name=staff_name)
    print('------user_details----',user_details)
    service_instance = srvc.objects.get(svname=service)
    user_service_detail_instance= user_service_details.objects.get(service=service_instance, user_id=request.user.id)
    user_service_detail_instance.call_back_request=1
    user_service_detail_instance.save()
    user_notification_instance=user_notification.objects.get_or_create(
        recepient=user_details,sender=sender,service=service_instance,
        message=message,timestamp=timestamp,is_viewed=0)
    
    return redirect('myservice')
    
def all_service(request):
    return render(request,'User/user_dashboard/all_service.html')

def payments(request):
    pay = user_service_details.objects.filter(user_id=request.user.id)

    return render(request,'User/user_dashboard/payments.html',{'pay':pay})

def appointment(request):
    return render(request,'User/consultation.html')


def select_service(request,value=''):
    current_user = request.user
    return render(request,'User/user_dashboard/consultation.html',{'value':value})
    

def booking(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        num = request.POST['num']
        serv = request.POST['ser']
        msg = request.POST['msg']
        u = request.user
        service = srvc.objects.get(svname=serv)
        user_instance,user_created = CustomUser.objects.get_or_create(email=email,defaults={'name':name,'email':email,'phone_number':num })
        if userdata.objects.filter(email=u).exists() and userdata.objects.filter(phone_number='').exists():
            user_up = userdata.objects.get(email=u)
            user_up.name = name
            user_up.phone_number = num
            user_up.status = 0
            user_up.save()
        
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
        current_user = request.user
        latest_service_details_id=user_service_details.objects.latest('id')
        service_details_id = latest_service_details_id.id
        instance = user_service_details.objects.get(pk = service_details_id)
        if pay == 'on':
            instance.payment=True
        else:
            instance.payment=False    
        instance.save()
        if pay:
            serv = request.session.get('service_id_data', None)
            service = srvc.objects.get(svname=serv)
            d = DocumentsRequired.objects.filter( Service = service.svid)
            request.session['form_submitted'] = False
            return render(request,'User/user_dashboard/docu_upload.html',{'form':d,'head':serv})
        else:
            return  HttpResponse('<center><h1 style="color:red">Payment Failed</h1></center>')
    else:
        redirect('payment')

def upload_doc(request):
    
    if request.method == 'POST':
        received_data = request.session.get('user_id_data', None)
        ser_type = request.POST['ser_type']
        userid = request.POST['userid']
        serid = srvc.objects.get(svname=ser_type)
        ser_count = DocumentsRequired.objects.filter(Service=serid)
        """user_id = userdata.objects.get(id=userid)
        for i in ser_count:
            f1 = request.FILES[i.DocumentName]
            u = docu_all.objects.create(user=user_id,docu_file=f1)
            u.save()"""
        import os
        folder_path = os.path.join(os.getcwd(), "static", "docu_img")

        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path)
                print(f"Folder '{folder_path}' created successfully.")
            except OSError as e:
                print(f"Error creating folder '{folder_path}': {e}")
        else:
            print(f"Folder '{folder_path}' already exists.")

        
        documents = {}
        print(request.FILES.items())
        for document_name, uploaded_file in request.FILES.items():
            documents[document_name] = uploaded_file.name
            

                # Set the destination path within the "docu_img" folder
            destination_path = os.path.join(folder_path, uploaded_file.name)

                # Move the uploaded file to the destination path
            with open(destination_path, 'wb') as destination_file:
                for chunk in uploaded_file.chunks():
                    destination_file.write(chunk)
                  
        latest_service_details_id=user_service_details.objects.latest('id')
        service_details_id = latest_service_details_id.id
        instance = user_service_details.objects.get(pk = service_details_id)
        instance.documents=documents
        instance.save()
        # messages.success(request,"File uploaded successfully")
        # return redirect('upload_doc')
        request.session['form_submitted'] = True
        return redirect('upload_doc')
    
    else:
        # messages.error(request,"Failed to upload the file")
        # return redirect('upload_doc')
       
        return render(request,'User/user_dashboard/docu_upload.html',{'docu_err' :"Error to upload"})
        # return render(request, 'your_template.html')
    # return HttpResponse(f"Key: {key}, Value: {value} received successfully.")
    # return HttpResponse('<center><h1>Thankyou</h1></center>')