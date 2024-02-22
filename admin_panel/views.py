from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage
import logging
from .models import *
from django.forms.models import model_to_dict

# from user_portal.models import *
from .form import *
from django.contrib import messages
import os
from twilio.rest import Client


from django.core.mail import EmailMultiAlternatives,get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def success(request):
    return render(request, 'success_page.html')


def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_det = authenticate(request, username=username, password=password)
        if user_det is not None:
            user = get_object_or_404(User, username=username)
            if user.is_authenticated:

                login(request, user_det)
                if user.is_superuser:
                    
                    return redirect('admin:index')  # Redirect to the Django admin page after successful login
                else:
                    return redirect('/dashboard/')
        else:
            # Handle invalid login credentials
            return render(request, 'admin/main_app/login.html', {'error_message': 'Invalid credentials'})
    return render(request, 'admin/main_app/login.html')


def Logout(request):
    logout(request)
    return redirect('/')

@login_required(login_url="/")
def currency(request):
    if request.method == 'POST':
        frm = crncForm(request.POST)
        if frm.is_valid:
            instance = frm.save(commit=False)
            instance.usrid = request.user
            instance.save()
            return redirect('currency')
    else:
        frm = crncForm()
    model_meta = crnc._meta
    field_names = [field.verbose_name for field in model_meta.fields]
    y=crnc.objects.all()
    page=Paginator(y,5)
    page_list=request.GET.get('page')
    page=page.get_page(page_list)
    cou=UserProfile.objects.filter(taken_by__exact='').count()
    return render(request,'admin/super_user/currency.html',{'form': frm,'currency_info':page,'field_names': field_names,'cou':cou})


#delete currency
def del_currency(request,id):
    currency = crnc.objects.filter(pk=id)
    currency.delete()
    return redirect('currency')


#update currency
def update_currency(request,id):

    if request.method=='POST':
        currency=crnc.objects.get(pk=id)
        frm=crncForm(request.POST,instance=currency)
        if frm.is_valid:
            instance = frm.save(commit=False)
            instance.usrid = request.user
            instance.save()
            return redirect('currency')
    else:
        id = request.GET['id']
        print(id)
        currency=crnc.objects.get(pk=id)
        frm = crncForm(instance=currency)
        frm = str(frm)
        return JsonResponse({'success': True, 'form':frm})

# category
@login_required(login_url="/")
def category(request):
    if request.method == 'POST':
        ctrgy_frm = ctgryForm(request.POST,request.FILES)
        if ctrgy_frm.is_valid:
            instance = ctrgy_frm.save(commit=False)
            instance.usrid = request.user
            instance.save()
            return redirect('category')          
    else:        
        ctrgy_frm = ctgryForm() 
        
    model_meta = ctgry._meta
    field_names = [field.verbose_name for field in model_meta.fields]
    y=ctgry.objects.all()
    page=Paginator(y,5)
    page_list=request.GET.get('page')
    page=page.get_page(page_list)  
    cou=UserProfile.objects.filter(taken_by__exact='').count()
    return render(request,'admin/super_user/category.html',{'form': ctrgy_frm,'category_info':page,'field_names': field_names,'cou':cou})

#Delete Category
def del_category(request,id):
    category=ctgry.objects.filter(pk=id)
    category.delete()
    return redirect('category')

# Update Category
def update_category(request,id):

    if request.method == 'POST':
        updt_category=ctgry.objects.get(pk=id)
        ctgry_frm= ctgryForm(request.POST,request.FILES,instance=updt_category)
        if ctgry_frm.is_valid:
            instance=ctgry_frm.save(commit=False)
            instance.usrid=request.user
            instance.save()
            return redirect('category')
    else:
        id = request.GET['id']
        currency=ctgry.objects.get(pk=id)
        frm = ctgryForm(instance=currency)
        frm = str(frm)
        return JsonResponse({'success': True, 'form':frm})

@login_required(login_url="/")
def country(request):
    if request.method == 'POST':
        cntry_frm = cntryForm(request.POST)
        if cntry_frm.is_valid:
            instance = cntry_frm.save(commit=False)
            instance.usrid = request.user
            instance.save()
            return redirect('country')
    else:
        cntry_frm = cntryForm()
        
    model_meta = cntry._meta
    field_names = [field.verbose_name for field in model_meta.fields]
    y=cntry.objects.all()
    page=Paginator(y,5)
    page_list=request.GET.get('page')
    page=page.get_page(page_list)    
    #country_info=cntry.objects.all()
    cou=UserProfile.objects.filter(taken_by__exact='').count()
    return render(request,'admin/super_user/country.html',{'form': cntry_frm,'country_info':page,'field_names': field_names})
    
    
# Delete Country
def delete_country(request,id):
    country=cntry.objects.filter(pk=id)
    country.delete()
    return redirect('country')

#Update Country
def update_country(request,id):

    if request.method =="POST":
        updt_country=cntry.objects.get(pk=id)
        cntry_frm = cntryForm(request.POST,instance=updt_country)
        if cntry_frm.is_valid:
            instance=cntry_frm.save(commit=False)
            instance.usrid=request.user
            instance.save()
            return redirect('country')
    else:
        id = request.GET['id']
        print(id)
        currency=cntry.objects.get(pk=id)
        frm =cntryForm(instance=currency)
        frm = str(frm)
        return JsonResponse({'success': True, 'form':frm})


#document
@login_required(login_url="/")
def document(request):
    if request.method == 'POST':
        frm = DocumentForm(request.POST)
        if frm.is_valid:
            instance = frm.save(commit=False)
            instance.usrid = request.user
            instance.save()
            return redirect('document')
    else:
        frm = DocumentForm()
    model_meta = DocumentsRequired._meta
    field_names = [field.verbose_name for field in model_meta.fields]
    y=DocumentsRequired.objects.all()
    page=Paginator(y,5)
    page_list=request.GET.get('page')
    page=page.get_page(page_list)
    cou=UserProfile.objects.filter(taken_by__exact='').count()
    return render(request,'admin/super_user/document.html',{'form': frm,'document_info':page,'field_names': field_names,'cou':cou})


#delete document
def del_document(request,id):
    service=DocumentsRequired.objects.filter(pk=id)
    service.delete()
    return redirect('document')


#update document
def update_document(request,id):
    if request.method =="POST":
        updt_service=DocumentsRequired.objects.get(pk=id)
        srvc_frm = DocumentForm(request.POST,instance=updt_service)
        if srvc_frm.is_valid:
            instance=srvc_frm.save(commit=False)
            instance.usrid=request.user
            instance.save()
            return redirect('document')
    else:
        id = request.GET['id']
        print(id)
        currency=DocumentsRequired.objects.get(pk=id)
        frm =DocumentForm(instance=currency)
        frm = str(frm)
        return JsonResponse({'success': True, 'form':frm})


@login_required(login_url="/")
def services(request):
    error_message=""
    if request.method == 'POST':
        srvc_frm = srvcForm(request.POST)

        if srvc_frm.is_valid:
            err =srvc_frm.errors
            err=str(err)
            
            try:
                srvc_frm.usrid = request.user
                srvc_frm.save()
                return redirect('services')
            except ValueError as e:
                return JsonResponse({'success': False,'error_msg': err}) 

    else:
        srvc_frm = srvcForm()
    model_meta = srvc._meta
    field_names = [field.verbose_name for field in model_meta.fields]
    y=srvc.objects.all()
    page=Paginator(y,5)
    page_list=request.GET.get('page')
    page=page.get_page(page_list)
    cou=UserProfile.objects.filter(taken_by__exact='').count()
    return render(request,'admin/super_user/services.html',{'form': srvc_frm,'service_info':page,'field_names': field_names,'cou':cou})

#Delete Service
def delete_service(request,id):
    service=srvc.objects.filter(pk=id)
    service.delete()
    return redirect('services')

def Update_service(request,id):

    if request.method =="POST":
        updt_service=srvc.objects.get(pk=id)
        srvc_frm = srvcForm(request.POST,instance=updt_service)
        if srvc_frm.is_valid:
            srvc_frm = srvcForm(request.POST,instance=updt_service)
            instance=srvc_frm.save(commit=False)
            instance.usrid=request.user
            instance.save()
            return redirect('services')
    else:
        id = request.GET['id']
        currency=srvc.objects.get(pk=id)
        frm =srvcForm(instance=currency)
        frm = str(frm)
        return JsonResponse({'success': True, 'form':frm})

# Tax Details
@login_required(login_url="/")
def taxdetails(request):
    if request.method == 'POST':
        frm = TaxdeailsForm(request.POST)
        if frm.is_valid:
            instance=frm.save(commit=False)
            instance.usrid=request.user
            instance.save()
            return redirect('taxdetails')
    else:
        frm = TaxdeailsForm()
    model_meta = txdet._meta
    field_names = [field.verbose_name for field in model_meta.fields]
    y=txdet.objects.all()
    page=Paginator(y,5)
    page_list=request.GET.get('page')
    page=page.get_page(page_list)
    cou=UserProfile.objects.filter(taken_by__exact='').count()
    return render(request,'admin/super_user/taxdetails.html',{'form': frm,'taxdetail_info':page,'field_names': field_names,'cou':cou})

# del taxdetails
def delete_taxdetails(request,id):
    service=txdet.objects.filter(pk=id)
    service.delete()
    return redirect('taxdetails')

#update taxdetails
def update_taxdetails(request,id):
    if request.method =="POST":
        updt_service=txdet.objects.get(pk=id)
        srvc_frm = TaxdeailsForm(request.POST,instance=updt_service)
        if srvc_frm.is_valid:
            instance=srvc_frm.save(commit=False)
            instance.usrid=request.user
            instance.save()
            return redirect('taxdetails')
    else:
        id = request.GET['id']
        print(id)
        currency=txdet.objects.get(pk=id)
        frm = TaxdeailsForm(instance=currency)
        frm = str(frm)
        return JsonResponse({'success': True, 'form':frm})


# Tax Master
@login_required(login_url="/")
def taxmaster(request):
    if request.method == 'POST':
        frm = Tax_masterForm(request.POST)
        if frm.is_valid:
            instance=frm.save(commit=False)
            instance.usrid=request.user
            instance.save()
            return redirect('taxmaster')
    else:
        frm = Tax_masterForm()
    model_meta = txmst._meta
    field_names = [field.verbose_name for field in model_meta.fields]
    y=txmst.objects.all()
    page=Paginator(y,5)
    page_list=request.GET.get('page')
    page=page.get_page(page_list)
    cou=UserProfile.objects.filter(taken_by__exact='').count()
    return render(request,'admin/super_user/taxmaster.html',{'form': frm,'tax_info':page,'field_names': field_names,'cou':cou})


# del tax Master
def delete_taxmaster(request,id):
    service=txmst.objects.filter(pk=id)
    service.delete()
    return redirect('taxmaster')


#update taxdetails
def update_taxmaster(request,id):
    if request.method =="POST":
        updt_service=txmst.objects.get(pk=id)
        srvc_frm = Tax_masterForm(request.POST,instance=updt_service)
        if srvc_frm.is_valid:
            instance=srvc_frm.save(commit=False)
            instance.usrid=request.user
            instance.save()
            return redirect('taxmaster')
    else:
        id = request.GET['id']
        print(id)
        currency=txmst.objects.get(pk=id)
        frm = Tax_masterForm(instance=currency)
        frm = str(frm)
        return JsonResponse({'success': True, 'form':frm})


# @login_required(login_url="/")
def dashboard(request):
    cou=UserProfile.objects.filter(taken_by__exact='').count()
    total_order = UserProfile.objects.filter().count()
    
    model_meta = UserProfile._meta    
    field_names = [field.verbose_name for field in model_meta.fields 
                   if field.verbose_name not in ['Upload Document(.pdf)','Upload Image(.jpg/.jpeg)','Status']]
    latest_record = UserProfile.objects.all().order_by('-created_at')[:5]
    
    return render(request,'admin/main_app/main_layout.html',{'cou':cou,'total':total_order,
                                              "latest_data":latest_record,"field_names":field_names})


from user_portal.models import *
def orders(request,):    
    model_meta = user_service_details._meta
    field_names = [field.verbose_name for field in model_meta.fields]
    
    # Get all objects where taken_by is blank
    objects_with_blank_taken_by = user_service_details.objects.filter(taken_by='')
    
    page=Paginator(objects_with_blank_taken_by,5)
    page_list=request.GET.get('page')
    page=page.get_page(page_list)
    cou=user_service_details.objects.filter(taken_by__exact='').count()
    return render(request,'admin/staff/orders.html',{'order_info':page,'field_names': field_names,'cou':cou})

#user demo
def demo_user(request):
    if request.method == 'POST':
        frm = userForm(request.POST, request.FILES)
        if frm.is_valid:
            frm.save()
            return redirect('demo_user')
    else:
        frm = userForm()
    return render(request,"admin/super_user/user.html",{'form':frm})


""" function for listing the selected task """
def my_task(request):
    model_meta = user_service_details._meta
    field_names = [field.verbose_name for field in model_meta.fields]
    y=user_service_details.objects.filter(taken_by=request.user)
    page=Paginator(y,5)
    page_list=request.GET.get('page')
    page=page.get_page(page_list)
    print(messages)
    cou=user_service_details.objects.filter(taken_by=request.user).count()
    return render(request,'admin/staff/task.html',{'task_info':page,'field_names': field_names,'cou':cou})


"""function to select task from order list"""
def select_my_task(request,id):
    model_meta = user_service_details._meta
    field_names = [field.verbose_name for field in model_meta.fields]
   
    instance = user_service_details.objects.get(pk=id)  # Replace 1 with the actual primary key value
    print("----------->>>>>>>>>>",request.user.username)
    instance.taken_by = request.user.username # Update the values of the fields
    instance.save()   # Save the changes to the database
    messages.success(request,"sucess") 
    
    """code to send mail to user when staff select the particular task """
    context={"user_name":instance.user_id}
    connection = get_connection() # uses SMTP server specified in settings.py
    connection.open() # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()
    user_id = userdata.objects.get(name=instance.user_id)
    print(user_id.email)
    print(user_id.phone_number)
    html_content = render_to_string('admin/main_app/email_template.html', context)               
    text_content = strip_tags(html_content)  # Strip HTML tags for the plain text version                  
    msg = EmailMultiAlternatives("Approval", text_content, "vasudevankarthik9@gmail.com",[user_id.email],connection=connection)                                      
    msg.attach_alternative(html_content, "text/html")  
    
    try:    # msg.content_subtype="html"                                                                                                                                                                             
        msg.send()        
    except Exception as e:
        print(f"==============>>>>>>>>>Error sending email: {e}")   
         
    connection.close()
    return redirect("task")


"""function to view the tasks"""

def task_details(request,id):
    model_meta = user_service_details._meta
    field_names = [field.verbose_name for field in model_meta.fields]
    task_detail=user_service_details.objects.get(pk=id)
    user_detail=userdata.objects.get(id=task_detail.user_id.id)
    service_name=srvc.objects.get(pk=task_detail.service.svid)
    user_data_dict = model_to_dict(task_detail)
    user_data_dict['service']=service_name
    user_data_dict['user_id']=user_detail
    user_data_dict['Name']=user_data_dict.pop('user_id')
    print('-------------',user_data_dict['documents'])
    filter_key=['id','msg','taken_by','status']
    filtered_user_data_dict = {key: value for key, value in user_data_dict.items() if key not in filter_key}
    print('-------------',filtered_user_data_dict)
    return render(request,"admin/staff/task_details.html",{"user_detail":user_detail,'field_names':field_names,'task_detail':filtered_user_data_dict})


def profile(request):
    return render(request,'profile.html')

""" function to list the total number of orders """
def total_ord(request):
    cou=user_service_details.objects.filter()
    sel=''
    if request.method == 'POST':
        sel = request.POST['opt']
        if sel == 'accept':
            cou=user_service_details.objects.exclude(taken_by='')
            sel='acc'
            print(cou)
        elif sel == 'pending':
            sel="pen"
            cou=user_service_details.objects.filter(taken_by__exact='')
        else:
            sel='all'
            cou=user_service_details.objects.filter()

    model_meta = user_service_details._meta
    field_names = [field.verbose_name for field in model_meta.fields if field.verbose_name not in ['Upload Document(.pdf)','Upload Image(.jpg/.jpeg)','Status']]
    page=Paginator(cou,8)
    page_list=request.GET.get('page')
    page=page.get_page(page_list)
    cou=user_service_details.objects.filter(taken_by__exact='').count()
    return render(request,'admin/staff/total_order.html',{'total_info':page,'field_names': field_names,'cou':cou,'sel':sel})
    


