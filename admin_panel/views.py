from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from .form import *

def Login(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_det = authenticate(request, username=username, password=password)
        user = get_object_or_404(User, username=username)
        
        if user_det is not None:
            if user.is_superuser:
                login(request, user_det)
                # Explicitly set the session to save the changes
                request.session.save()
                # Redirect to the Django admin page after successful login
                return redirect('admin:index')
            else:
                return render(request, 'main_layout.html',{'user':user})
            
        else:
            # Handle invalid login credentials
            return render(request, 'admin/login.html', {'error_message': 'Invalid credentials'})

    return render(request, 'admin/login.html')

# from django.shortcuts import render

# Create your views here.


# def index(request):
#     #  return redirect('/admin/')
#     return render(request,'admin.html')

def currency(request):
    if request.method == 'POST':
        frm = crncForm(request.POST)
        
        if frm.is_valid:
            frm.save()
            return redirect('success_url')
    else:
        frm = crncForm()
        
        
    model_meta = crnc._meta
    field_names = [field.verbose_name for field in model_meta.fields]
        
    currency_info=crnc.objects.all()
    
    return render(request,'currency.html',{'form': frm,'currency_info':currency_info,'field_names': field_names})



def category(request):
    if request.method == 'POST':
        frm = CategoryForm(request.POST)
        
        if frm.is_valid:
            frm.save()
            return redirect('success_url')
    else:
        frm = CategoryForm()
        
    model_meta = ctgry._meta
    field_names = [field.verbose_name for field in model_meta.fields]
        
    currency_info=ctgry.objects.all()
    return render(request,'category.html',{'form': frm,'currency_info':currency_info,'field_names': field_names})



def country(request):
    if request.method == 'POST':
        frm = CountryForm(request.POST)
        
        if frm.is_valid:
            frm.save()
            return redirect('success_url')
    else:
        frm = CountryForm()
        
    model_meta = cntry._meta
    field_names = [field.verbose_name for field in model_meta.fields]
        
    currency_info=cntry.objects.all()
    return render(request,'country.html',{'form': frm,'currency_info':currency_info,'field_names': field_names})

def document(request):
    return render(request,'document.html')


def services(request):
    if request.method == 'POST':
        frm = ServiceForm(request.POST)
        
        if frm.is_valid:
            frm.save()
            return redirect('success_url')
    else:
        frm = ServiceForm()
        
    model_meta = srvc._meta
    field_names = [field.verbose_name for field in model_meta.fields]
        
    currency_info=srvc.objects.all()
    return render(request,'services.html',{'form': frm,'currency_info':currency_info,'field_names': field_names}) 

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
    
    
    