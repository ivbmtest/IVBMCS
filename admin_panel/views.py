from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import logging
from .models import *
from .form import *


def success(request):
    return render(request, 'success_page.html')

# @login_required(login_url="/login/")
def Login(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_det = authenticate(request, username=username, password=password)
        user = get_object_or_404(User, username=username)
        
        if user.is_authenticated:
            if user_det is not None:
                login(request, user_det)
                request.session.save()
                if user.is_superuser:
                      # Explicitly set the session to save the changes
                    return redirect('admin:index')  # Redirect to the Django admin page after successful login
                else:
                    # print(user.id)
                    print("----------->>>>>>>--",user.id)
                    return render(request, 'admin.html',{'user':user})
            
        else:
            # Handle invalid login credentials
            return render(request, 'admin/login.html', {'error_message': 'Invalid credentials'})

    return render(request, 'admin/login.html')


def currency(request):
    if request.method == 'POST':
        frm = crncForm(request.POST)
        
        if frm.is_valid:
            frm.save()
            return redirect('currency')
    else:
        frm = crncForm()
        
    model_meta = crnc._meta
    field_names = [field.verbose_name for field in model_meta.fields]
        
    currency_info=crnc.objects.all()
    return render(request,'currency.html',{'form': frm,'currency_info':currency_info,'field_names': field_names})


#delete currency
def del_currency(request,id):
    currency = crnc.objects.filter(pk=id)
    currency.delete()
    return redirect('currency')

#update currency
def update_currency(request,id):
    currency=crnc.objects.get(pk=id)
    if request.method=='POST':
        frm=crncForm(request.POST,instance=currency)
        if frm.is_valid:
            frm.user = request.user
            frm.save()
            return redirect('currency')
    else:
        frm = crncForm(instance=currency)
        
    model_meta = crnc._meta
    field_names = [field.verbose_name for field in model_meta.fields]
        
    currency_info=crnc.objects.all()
    for i in currency_info:
        print("======>>>>-----")
    return render(request,'currency.html',{'form': frm,'currency_info':currency_info,'field_names': field_names})
        
    # return render(request,'currency.html',{'form': frm})
               

def category(request):
    if request.method == 'POST':
        ctrgy_frm = ctgryForm(request.POST,request.FILES)
        
        if ctrgy_frm.is_valid:
            ctrgy_frm.save()
            return redirect('category')
                    
    else:        
        ctrgy_frm = ctgryForm()
        
    model_meta = ctgry._meta
    field_names = [field.verbose_name for field in model_meta.fields]
        
    category_info=ctgry.objects.all()
    return render(request,'category.html',{'form': ctrgy_frm,'category_info':category_info,'field_names': field_names})

#Delete Category
def del_category(request,id):
    category=ctgry.objects.filter(pk=id)
    category.delete()
    return redirect('category')

# Update Category
def update_category(request,id):
    updt_category=ctgry.objects.get(pk=id)
    
    if request.method == 'POST':
        ctgry_frm= ctgryForm(request.POST,request.FILES,instance=updt_category)
        if ctgry_frm.is_valid:
            instance=ctgry_frm.save(commit=False)
            instance.usrid=request.user
            instance.save()
            return redirect('category')
        else:
            ctgry_frm= ctgryForm(instance=updt_category)
            
    model_meta = ctgry._meta
    field_names = [field.verbose_name for field in model_meta.fields]
        
    category_info=ctgry.objects.all()
    return render(request,'category.html',{'form': ctgry_frm,'category_info':category_info,'field_names': field_names})
      
            
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
        
    country_info=cntry.objects.all()
    return render(request,'country.html',{'form': cntry_frm,'country_info':country_info,'field_names': field_names})

# Delete Country
def delete_country(request,id):
    country=cntry.objects.filter(pk=id)
    country.delete()
    return redirect('country')

#Update Country
def update_country(request,id):
    updt_country=cntry.objects.get(pk=id)
    
    if request.method =="POST":
        cntry_frm = cntryForm(request.POST,instance=updt_country)
        if cntry_frm.is_valid:
            instance=cntry_frm.save(commit=False)
            instance.usrid=request.user
            instance.save()
            return redirect('country')
        else:
            ctgry_frm= cntryForm(instance=updt_country)
            
    model_meta = cntry._meta
    field_names = [field.verbose_name for field in model_meta.fields]
        
    country_info=cntry.objects.all()
    return render(request,'country.html',{'form': cntry_frm,'country_info':country_info,'field_names': field_names})
      
            

def document(request):
    return render(request,'document.html')


def services(request):
    if request.method == 'POST':
        srvc_frm = srvcForm(request.POST)
        
        if srvc_frm.is_valid:
            print("--------valid svc")
            # instance = srvc_frm.save(commit=False)
            print('invalid svc===========>>>>>>>',srvc_frm.errors)
            try:
                srvc_frm.usrid = request.user
                srvc_frm.save()
                return redirect('services')
            except ValueError as e:
                print("----------------exception.............")
                # logging.error(f"Error saving model: {e}")                     
                          
            
    else:
        # print('invalid svc===========>>>>>>>',srvc_frm.errors)
        srvc_frm = srvcForm()
        
    model_meta = srvc._meta
    field_names = [field.verbose_name for field in model_meta.fields]
        
    service_info=srvc.objects.all()
    return render(request,'services.html',{'form': srvc_frm,'service_info':service_info,'field_names': field_names})

#Delete Service
def delete_service(request,id):
    service=srvc.objects.filter(pk=id)
    service.delete()
    return redirect('services')

def Update_service(request,id):
    updt_service=srvc.objects.get(pk=id)
    
    if request.method =="POST":
        srvc_frm = srvcForm(request.POST,instance=updt_service)
        if srvc_frm.is_valid:
            instance=srvc_frm.save(commit=False)
            instance.usrid=request.user
            instance.save()
            return redirect('services')
        else:
            srvc_frm= srvcForm(instance=updt_service)
        
    model_meta = srvc._meta
    field_names = [field.verbose_name for field in model_meta.fields]
        
    service_info=cntry.objects.all()
    return render(request,'services.html',{'form': srvc_frm,'service_info':service_info,'field_names': field_names})

            
            

def dashboard(request):
    return render(request,'main_layout.html')

def logout(request):
    return render(request,'admin/login.html')


# def crncform(request):
#     if request.method == 'POST':
#         frm = crncForm(request.POST)
        
#         if frm.is_valid:
#             frm.save()
#             return redirect('success_url')
#     else:
#         frm = crncForm()
        
#     return render(request, 'currency.html', {'form': frm})



# def db_details(request):
    
    
    