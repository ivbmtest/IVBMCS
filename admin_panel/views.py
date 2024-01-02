from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage
import logging
from .models import *
from .form import *


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
                      # Explicitly set the session to save the changes
                    return redirect('admin:index')  # Redirect to the Django admin page after successful login
                else:
                    # print(user.id)
                    # print("----------->>>>>>>--",user.id)
                    #return render(request, 'admin.html',{'user':user})
                    return redirect('/dashboard/')   
        else:
            # Handle invalid login credentials
            return render(request, 'admin/login.html', {'error_message': 'Invalid credentials'})
    return render(request, 'admin/login.html')


def Logout(request):
    logout(request)
    return redirect('/')

def index(request):  
    student = crncForm()  
    return render(request,"forms.html",{'form':student})  

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
        y=crnc.objects.all()
        page=Paginator(y,5)
        page_list=request.GET.get('page')
        page=page.get_page(page_list)
        print(page)
        #currency_info=crnc.objects.all()
        return render(request,'currency.html',{'form': frm,'currency_info':page,'field_names': field_names})


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
            frm.user = request.user
            frm.save()
            return redirect('currency')
    else:
        id = request.GET['id']
        print(id)
        currency=crnc.objects.get(pk=id)
        frm = crncForm(instance=currency)
        frm = str(frm)
        return JsonResponse({'success': True, 'form':frm})

# category
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
        y=ctgry.objects.all()
        page=Paginator(y,5)
        page_list=request.GET.get('page')
        page=page.get_page(page_list)  
        #category_info=ctgry.objects.all()
        return render(request,'category.html',{'form': ctrgy_frm,'category_info':page,'field_names': field_names})

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
        y=cntry.objects.all()
        page=Paginator(y,5)
        page_list=request.GET.get('page')
        page=page.get_page(page_list)    
        #country_info=cntry.objects.all()
        return render(request,'country.html',{'form': cntry_frm,'country_info':page,'field_names': field_names})
    
    
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
      
            
#document
def document(request):
    if request.method == 'POST':
        frm = DocumentForm(request.POST)
        if frm.is_valid:
            frm.save()
            print("fs")
            return redirect('document')
    else:
        frm = DocumentForm()
        model_meta = DocumentsRequired._meta
        field_names = [field.verbose_name for field in model_meta.fields] 
        y=DocumentsRequired.objects.all()
        page=Paginator(y,5)
        page_list=request.GET.get('page')
        page=page.get_page(page_list)  
        return render(request,'document.html',{'form': frm,'document_info':page,'field_names': field_names})


#delete document
def del_document(request,id):
    service=DocumentsRequired.objects.filter(pk=id)
    service.delete()
    return redirect('document')


#update document
def update_document(request,id):
    updt_service=DocumentsRequired.objects.get(pk=id)
    if request.method =="POST":
        srvc_frm = DocumentForm(request.POST,instance=updt_service)
        if srvc_frm.is_valid:
            instance=srvc_frm.save(commit=False)
            instance.usrid=request.user
            instance.save()
            return redirect('document')
        else:
            srvc_frm= DocumentForm(instance=updt_service)
    model_meta = DocumentsRequired._meta
    field_names = [field.verbose_name for field in model_meta.fields]    
    service_info=DocumentsRequired.objects.all()
    return render(request,'document.html',{'form': srvc_frm,'service_info':service_info,'field_names': field_names})




def services(request):
    error_message=""
    if request.method == 'POST':
        srvc_frm = srvcForm(request.POST)
        
        if srvc_frm.is_valid:
            print('invalid svc===========>>>>>>>',srvc_frm.errors)
            try:
                srvc_frm.usrid = request.user
                srvc_frm.save()
                return redirect('services')
            except ValueError as e:
                print("----------------exception.............")
                 
                return render(request,'services.html',{'form': srvc_frm,'error_msg': error_message})
                                 
    else:
       
        srvc_frm = srvcForm()  
        
    model_meta = srvc._meta
    field_names = [field.verbose_name for field in model_meta.fields]
    y=srvc.objects.all()
    page=Paginator(y,5)
    page_list=request.GET.get('page')
    page=page.get_page(page_list)     
    return render(request,'services.html',{'form': srvc_frm,'service_info':page,'field_names': field_names})


#Delete Service
def delete_service(request,id):
    service=srvc.objects.filter(pk=id)
    service.delete()
    return redirect('services')

def Update_service(request,id):
    error_message=""
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

            
# Tax Details
def taxdetails(request):
    if request.method == 'POST':
        frm = TaxdeailsForm(request.POST)
        if frm.is_valid:
            frm.save()
            return redirect('taxdetails')
    else:
        frm = TaxdeailsForm()
        model_meta = txdet._meta
        field_names = [field.verbose_name for field in model_meta.fields]   
        y=txdet.objects.all()
        page=Paginator(y,5)
        page_list=request.GET.get('page')
        page=page.get_page(page_list)
        return render(request,'taxdetails.html',{'form': frm,'taxdetail_info':page,'field_names': field_names})

# del taxdetails
def delete_taxdetails(request,id):
    service=txdet.objects.filter(pk=id)
    service.delete()
    return redirect('taxdetails')

#update taxdetails
def update_taxdetails(request,id):
    updt_service=txdet.objects.get(pk=id)
    if request.method =="POST":
        srvc_frm = TaxdeailsForm(request.POST,instance=updt_service)
        if srvc_frm.is_valid:
            instance=srvc_frm.save(commit=False)
            instance.usrid=request.user
            instance.save()
            return redirect('taxdetails')
        else:
            srvc_frm= TaxdeailsForm(instance=updt_service)
    model_meta = txdet._meta
    field_names = [field.verbose_name for field in model_meta.fields]    
    service_info=txdet.objects.all()
    return render(request,'taxdetails.html',{'form': srvc_frm,'service_info':service_info,'field_names': field_names})


# Tax Master
def taxmaster(request):
    if request.method == 'POST':
        frm = Tax_masterForm(request.POST)
        if frm.is_valid:
            frm.save()
            return redirect('taxmaster')
    else:
        frm = Tax_masterForm()
        model_meta = txmst._meta
        field_names = [field.verbose_name for field in model_meta.fields]   
        y=txmst.objects.all()
        page=Paginator(y,5)
        page_list=request.GET.get('page')
        page=page.get_page(page_list)  
        return render(request,'taxmaster.html',{'form': frm,'tax_info':page,'field_names': field_names})


# del tax Master
def delete_taxmaster(request,id):
    service=txmst.objects.filter(pk=id)
    service.delete()
    return redirect('taxmaster')


#update taxdetails
def update_taxmaster(request,id):
    updt_service=txmst.objects.get(pk=id)
    if request.method =="POST":
        srvc_frm = Tax_masterForm(request.POST,instance=updt_service)
        if srvc_frm.is_valid:
            instance=srvc_frm.save(commit=False)
            instance.usrid=request.user
            instance.save()
            return redirect('taxmaster')
        else:
            srvc_frm= Tax_masterForm(instance=updt_service)
    model_meta = txmst._meta
    field_names = [field.verbose_name for field in model_meta.fields]    
    service_info=txmst.objects.all()
    return render(request,'taxmaster.html',{'form': srvc_frm,'service_info':service_info,'field_names': field_names})


def dashboard(request):
    return render(request,'main_layout.html')



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
    
    
    