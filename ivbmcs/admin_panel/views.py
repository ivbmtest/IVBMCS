from django.shortcuts import render, HttpResponse, redirect,get_object_or_404,reverse
from django.contrib.auth import login, logout,authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging
from .models import *
from .form import *
from django.contrib import messages
import os
from twilio.rest import Client
from user_portal.models import *
# from .backends import  EmailBackend
import datetime

from django.core.mail import EmailMultiAlternatives,get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags



def success(request):
    return render(request, 'success_page.html')


def Login(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        user_det = authenticate(request, email=email, password=password)
        if user_det is not None:
            user = get_object_or_404(CustomUser, email=email)            
            if user.is_authenticated:
                login(request, user_det)
                if user.user_type=='1':                    
                    return redirect('/dashboard/')  # Redirect to the admin Dashboard after successful login
                elif user.user_type == '2':  
                    return redirect('/staff_dashboard/') # Redirect to the Staff Dashboard page after successful login
                elif user.user_type == '3':  
                    return redirect('/age_home') # Redirect to the Agent Dashboard after successful login
        else:
            # Handle invalid login credentials
            return render(request, 'admin/main_app/login.html', {'error_message': 'Invalid credentials'})
    return render(request, 'admin/main_app/login.html')


def Logout(request):
    user = request.user.email
    user = get_object_or_404(CustomUser, email=user)
    if user.user_type == '4':
        logout(request)
        return redirect('/')
    else:
        logout(request)
        return redirect('/login')




@login_required(login_url="/")
def currency(request):
    if request.method == 'POST':
        print('-------------user::',request.user)
        frm = crncForm(request.POST)
        if frm.is_valid:
            instance = frm.save(commit=False)
            instance.id=request.user
            instance.save()
            return redirect('currency')
    else:
        frm = crncForm()
    model_meta = crnc._meta
    field_names = [field.verbose_name for field in model_meta.fields]
    y=crnc.objects.all()
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
    cou=UserProfile.objects.filter(taken_by__exact='').count()
    return render(request, 'admin/super_user/currency.html', {
        'form': frm,'currency_info':page,'field_names': field_names,'cou':cou,
        'start_index': start_index,"page_parameter": page_parameter,
        "paginate_parameter": paginate_parameter})
    # page=Paginator(y,5)
    # page_list=request.GET.get('page')
    # page=page.get_page(page_list)
    # cou=UserProfile.objects.filter(taken_by__exact='').count()
    # return render(request,'admin/super_user/currency.html',{'form': frm,'currency_info':page,'field_names': field_names,'cou':cou})
  


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
            instance.id = request.user.first_name
            print('------>',request.user)
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
          
          
            instance.id = request.user
            instance.save()
            return redirect('category')          
    else:        
        ctrgy_frm = ctgryForm() 
        
    model_meta = ctgry._meta
    field_names = [field.verbose_name for field in model_meta.fields]
    y=ctgry.objects.all()
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
    return render(request, 'admin/super_user/category.html', {
        'form': ctrgy_frm,'category_info':page,'field_names': field_names,
        'start_index': start_index,"page_parameter": page_parameter,
        "paginate_parameter": paginate_parameter})
    # page=Paginator(y,5)
    # page_list=request.GET.get('page')
    # page=page.get_page(page_list)  
    # cou=UserProfile.objects.filter(taken_by__exact='').count()
    # return render(request,'admin/super_user/category.html',{'form': ctrgy_frm,'category_info':page,'field_names': field_names,'cou':cou})
   

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
            instance.id=request.user
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
            instance.id = request.user
            instance.save()
            return redirect('country')
    else:
        cntry_frm = cntryForm()
        
        
    model_meta = cntry._meta
    field_names = [field.verbose_name for field in model_meta.fields]
    y=cntry.objects.all()    
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
    return render(request, 'admin/super_user/country.html', {
        'form': cntry_frm,'country_info':page,'field_names': field_names,
        'start_index': start_index,"page_parameter": page_parameter,
        "paginate_parameter": paginate_parameter})
    # page=Paginator(y,5)
    # page_list=request.GET.get('page')
    # page=page.get_page(page_list)    
    # #country_info=cntry.objects.all()
    # cou=UserProfile.objects.filter(taken_by__exact='').count()
    # return render(request,'admin/super_user/country.html',{'form': cntry_frm,'country_info':page,'field_names': field_names})
  
    
    
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
            instance.id=request.user
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
            instance.id = request.user
            instance.save()
            return redirect('document')
    else:
        frm = DocumentForm()
    model_meta = DocumentsRequired._meta
    field_names = [field.verbose_name for field in model_meta.fields]
    y=DocumentsRequired.objects.all()
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
    return render(request, 'admin/super_user/document.html', {
        'form': frm,'document_info':page,'field_names': field_names,
        'start_index': start_index,"page_parameter": page_parameter,
        "paginate_parameter": paginate_parameter})
    # page=Paginator(y,5)
    # page_list=request.GET.get('page')
    # page=page.get_page(page_list)
    # cou=UserProfile.objects.filter(taken_by__exact='').count()
    # return render(request,'admin/super_user/document.html',{'form': frm,'document_info':page,'field_names': field_names,'cou':cou})
   


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
            instance.id=request.user
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
                srvc_frm.id = request.user
                srvc_frm.save()
                return redirect('services')
            except ValueError as e:
                return JsonResponse({'success': False,'error_msg': err}) 
               

    else:
        srvc_frm = srvcForm()
    model_meta = srvc._meta
    field_names = [field.verbose_name for field in model_meta.fields]
    y=srvc.objects.all()
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
    return render(request, 'admin/super_user/services.html', {
        'form': srvc_frm,'service_info':page,'field_names': field_names,
        'start_index': start_index,"page_parameter": page_parameter,
        "paginate_parameter": paginate_parameter})
    # page=Paginator(y,5)
    # page_list=request.GET.get('page')
    # page=page.get_page(page_list)
   
    # return render(request,'admin/super_user/services.html',{'form': srvc_frm,'service_info':page,'field_names': field_names})
   

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
            instance.id=request.user
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
            instance.id=request.user
            instance.save()
            return redirect('taxdetails')
    else:
        frm = TaxdeailsForm()
    model_meta = txdet._meta
    field_names = [field.verbose_name for field in model_meta.fields]
    y=txdet.objects.all()
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
    return render(request,'admin/super_user/taxdetails.html', {
        'form': frm,'taxdetail_info':page,'field_names': field_names,
        'start_index': start_index,"page_parameter": page_parameter,
        "paginate_parameter": paginate_parameter})
    # page=Paginator(y,5)
    # page_list=request.GET.get('page')
    # page=page.get_page(page_list)
    # cou=UserProfile.objects.filter(taken_by__exact='').count()
    # return render(request,'admin/super_user/taxdetails.html',{'form': frm,'taxdetail_info':page,'field_names': field_names,'cou':cou})
    

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
            instance.id=request.user
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
            instance.id=request.user
            instance.save()
            return redirect('taxmaster')
    else:
        frm = Tax_masterForm()
    model_meta = txmst._meta
    field_names = [field.verbose_name for field in model_meta.fields]
    y=txmst.objects.all()
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
    return render(request, 'admin/super_user/taxmaster.html', {
        'form': frm,'tax_info':page,'field_names': field_names,
        'start_index': start_index,"page_parameter": page_parameter,
        "paginate_parameter": paginate_parameter})
    # page=Paginator(y,5)
    # page_list=request.GET.get('page')
    # page=page.get_page(page_list)
    # cou=UserProfile.objects.filter(taken_by__exact='').count()
    # return render(request,'admin/super_user/taxmaster.html',{'form': frm,'tax_info':page,'field_names': field_names,'cou':cou})
   


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
            instance.id=request.user
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
   
    cou=user_service_details.objects.filter(taken_by__isnull=True).count()
    total_order = user_service_details.objects.filter().count()
    take = user_service_details.objects.filter(taken_by__isnull=False).count()

    #user count
    admin = CustomUser.objects.filter(user_type=1).count()
    sta = CustomUser.objects.filter(user_type=2).count()
    age = CustomUser.objects.filter(user_type=3).count()
  
    model_meta = user_service_details._meta    
    # field_names = [field.verbose_name for field in model_meta.fields 
    #                if field.verbose_name not in ['user_id','Upload Document(.pdf)','Upload Image(.jpg/.jpeg)','Status']]
    latest_order = user_service_details.objects.all().order_by('-created_at')[:5]
    s = user_service_details.objects.all()
    
    li = [i.created_at.month for i in s if i.user_id.user_type == "4"]

    d = {i: li.count(i) if i in li else 0 for i in range(1, 13)}
    mon = [d[i] for i in range(1, 13)]

    return render(request,'admin/main_app/main_layout.html',{'cou':cou,'take':take,'total':total_order, "latest_order":latest_order,'data':mon,'sta':sta,'age':age,'admin':admin})


@login_required(login_url="/")
def orders(request):    
    model_meta = user_service_details._meta
    field_names = [field.verbose_name for field in model_meta.fields]
    y = user_service_details.objects.filter(taken_by__isnull=True)    
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
    print(start_index)
    return render(request, 'admin/super_user/orders.html', {
            'order_info': page, 'field_names': field_names, 'start_index': start_index,
            "page_parameter": page_parameter,
            "paginate_parameter": paginate_parameter})
    # if request.user.user_type == str(1):
        
    #     return render(request, 'admin/super_user/orders.html', {
    #         'order_info': page, 'field_names': field_names, 'start_index': start_index,
    #         "page_parameter": page_parameter,
    #         "paginate_parameter": paginate_parameter})
    # else:
        
    #     return render(request, 'admin/staff/orders.html', {
    #         'order_info': page, 'field_names': field_names, 'start_index': start_index,
    #         "page_parameter": page_parameter,
    #         "paginate_parameter": paginate_parameter})
        

   

    # return render(request, 'admin/staff/orders.html', {'order_info': page, 'field_names': field_names, 'start_index': start_index})

# def orders(request,):
#     model_meta =user_service_details._meta
#     field_names = [field.verbose_name for field in model_meta.fields]
#     y=user_service_details.objects.filter(taken_by__exact='')
#     # selected_value = request.POST.get('cars')
#     # print('---------selected val',selected_value)
#     # Update the data variable based on the selected value
#     # For example:
#     count_of_data=2
#     # if request.method == 'POST':
#     selected_value = request.POST.get('selected_value')  # 'cars' matches the name attribute of the <select> tag
#     print('---------selected val',selected_value)
#     # count_of_data=0
#     if selected_value is not None:
#         print('-------entered!!!')
#         try:
#             print('-------entered try!!!')
#             count_of_data = int(selected_value)
#             print('---------count_of_data',count_of_data)
#             page=Paginator(y,count_of_data)
#             page_list=request.GET.get('page')
#             page=page.get_page(page_list)
#             # cou=UserProfile.objects.filter(taken_by__exact='').count()
#             start_index = (page.number - 1) * count_of_data + 1
#             # print('-----page.number--->>>',page.number)
#             # print('-----page.number - 1--->>>',page.number - 1)
#             # print('-----len(page) --->>>',len(page))
#             # print('-----start_index--->>>',start_index)
#             return render(request, 'admin/staff/orders.html', {'order_info': page, 'field_names': field_names, 'start_index': start_index})
#             # You can perform any necessary actions with the updated data here
#             # return JsonResponse({'success': True, 'data': count_of_data})
#         except ValueError:
#             return JsonResponse({'success': False, 'error': 'Invalid value'})
#     else:
#     #     return JsonResponse({'success': False, 'error': 'No value selected'})
#     # count_of_data = int(selected_value)
#     # count_of_data=3 #indicates the count of data to be shown in one page
#         print('---------count_of_data',count_of_data)
#         page=Paginator(y,count_of_data)
#         page_list=request.GET.get('page')
#         page=page.get_page(page_list)
#         # cou=UserProfile.objects.filter(taken_by__exact='').count()
#         start_index = (page.number - 1) * count_of_data + 1
#         print('-----page.number--->>>',page.number)
#         print('-----page.number - 1--->>>',page.number - 1)
#         print('-----len(page) --->>>',len(page))
#         print('-----start_index--->>>',start_index)
#         return render(request, 'admin/staff/orders.html', {'order_info': page, 'field_names': field_names, 'start_index': start_index})
        


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
@login_required(login_url="/")
def my_task(request):
    model_meta = user_service_details._meta
    field_names = [field.verbose_name for field in model_meta.fields]
    
    y=user_service_details.objects.filter(taken_by=request.user.staff.id)
    
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
    return render(request, 'admin/staff/task.html', {
        'task_info':page,'field_names': field_names,
        'start_index': start_index,"page_parameter": page_parameter,
        "paginate_parameter": paginate_parameter})
    # return render(request,'admin/staff/task.html',{'task_info':page,'field_names': field_names,'cou':cou})
    


"""function to select task from order list"""

@login_required(login_url="/")

# when staff select a task send mail and admin assign staff send a mail both are here
def select_my_task(request,id):
    
    print("seleeeeeee",id)
    model_meta = UserProfile._meta
    model_meta = CustomUser._meta
    field_names = [field.verbose_name for field in model_meta.fields]
    current_user = request.user
    # notification_instance=user_notification.objects.get(pk=id)
    # user_details = CustomUser.objects.get(pk=notification_instance.user_id.id)
    task_instance = user_service_details.objects.get(pk=id)  # Replace 1 with the actual primary key value
    #admin assign
    request.session['staff_assigned'] = False
    
    if request.method == 'POST':
        staff_id = request.POST['staff']
        _staff = Staff.objects.get(pk=staff_id)
        task_instance.taken_by=_staff
        
        print("staff____",_staff.id)
        staff_taken = _staff.admin.id
        taken_mail = _staff.admin.email
        print("user_id",id)
        request.session['staff_assigned'] = True
        
        staff_instance=Staff.objects.get(pk=staff_id)
        print("staff_instance",staff_instance.id)
        task_instance.taken_by=staff_instance
        print("staff_id",staff_id)
        message = f'your request for {task_instance.service} is assigned to {staff_instance}'
    else:
        staff_taken = request.user.staff.id
        print("else")
        print(request.user.email)
        taken_mail  = request.user.email
        
        task_instance.taken_by=request.user.staff
    
    print('taken_mail',taken_mail)
    task_instance.save()
    user_details = CustomUser.objects.get(pk=task_instance.user_id.id)
    service_instance = srvc.objects.get(pk=task_instance.service.svid)
    time = datetime.datetime.now()
    message = f'your request for {task_instance} is taken by {current_user}'
    user_notification.objects.get_or_create(message=message, timestamp=time,recepient=user_details, service=service_instance,sender=taken_mail)
    # Update the values of the fields
    
    task_instance.save()   # Save the changes to the database
    
    """code to send mail to user when staff select the particular task """
 
    """code to send mail to user when staff select the particular task """
    context={"user_name":task_instance.user_id}
    
    #connection = get_connection() # uses SMTP server specified in settings.py
    #connection.open() # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()
    print('===========>>',task_instance.user_id.email)
    
    
    return redirect('task_detail', id=id)


"""function to view the tasks"""

@login_required(login_url="/")
def task_details(request,id):
    task=user_service_details.objects.get(pk=id)
    user_details=CustomUser.objects.get(pk=task.user_id.id)
    # staff_user = CustomUser.objects.filter(is_staff=True)
    
    staff = Staff.objects.all()
    
    return render(request,"admin/staff/task_details.html",{"task":task,'user_details':user_details,'staff':staff})
    

@login_required(login_url="/")
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
    
    


# State
@login_required(login_url="/")
def state(request):
    if request.method == 'POST':
        sta_frm = stateForm(request.POST)
        if sta_frm.is_valid:
            instance = sta_frm.save(commit=False)
            # instance.id = request.user
            instance.save()
            return redirect('state')
        else:
            print(sta_frm.errors)
    else:
        sta_frm = stateForm()
        
    model_meta = states._meta
    field_names = [field.verbose_name for field in model_meta.fields]
    y=states.objects.all()
    page=Paginator(y,5) 
    page_list=request.GET.get('page')
    page=page.get_page(page_list)    
    #country_info=cntry.objects.all()
    #cou=UserProfile.objects.filter(taken_by__exact='').count()
    return render(request,'admin/super_user/state.html',{'form': sta_frm,'state_info':page,'field_names': field_names})


#update state
def update_state(request,id):
    if request.method=='POST':
        state=states.objects.get(pk=id)
        frm=stateForm(request.POST,instance=state)
        if frm.is_valid:
            instance = frm.save(commit=False)
            # instance.id = request.user
            instance.save()
            return redirect('state')
    else:
        id = request.GET['id']
        print(id)
        state=states.objects.get(pk=id)
        frm = stateForm(instance=state)
        frm = str(frm)
        return JsonResponse({'success': True, 'form':frm})
    
#delete state
def del_state(request,id):
    state = states.objects.filter(pk=id)
    state.delete()
    return redirect('state')



# Format
@login_required(login_url="/")
def format(request):
    if request.method == 'POST':
        format_frm = Format_Form(request.POST)
        if format_frm.is_valid:
            instance = format_frm.save(commit=False)
            # instance.id = request.user
            instance.save()
            return redirect('format')
        else:
            print(format_frm.errors)
    else:
        format_frm = Format_Form()
        
    model_meta = formt._meta
    field_names = [field.verbose_name for field in model_meta.fields]
    y=formt.objects.all()
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
    return render(request, 'admin/super_user/format.html', {
        'form': format_frm,'format_info':page,'field_names': field_names,
        'start_index': start_index,"page_parameter": page_parameter,
        "paginate_parameter": paginate_parameter})
    # page=Paginator(y,5)    
    # page_list=request.GET.get('page')
    # page=page.get_page(page_list)    
    # #country_info=cntry.objects.all()
    # #cou=UserProfile.objects.filter(taken_by__exact='').count()
    # return render(request,'admin/super_user/format.html',{'form': format_frm,'format_info':page,'field_names': field_names})


#update currency
def update_format(request,id):
    if request.method=='POST':
        state=formt.objects.get(pk=id)
        frm=Format_Form(request.POST,instance=state)
        if frm.is_valid:
            instance = frm.save(commit=False)
            # instance.id = request.user
            instance.save()
            return redirect('format')
    else:
        id = request.GET['id']
        print(id)
        state=formt.objects.get(pk=id)
        frm = Format_Form(instance=state)
        frm = str(frm)
        return JsonResponse({'success': True, 'form':frm})
    
#delete currency
def del_format(request,id):
    state = formt.objects.filter(pk=id)
    state.delete()
    return redirect('format')

