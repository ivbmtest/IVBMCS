from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
#from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from .form import *
from django.db.models.query_utils import Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.forms.models import model_to_dict


def Login(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_det = authenticate(request, username=username, password=password)
        
        if user_det is not None:
            user = get_object_or_404(User, username=username)
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
        form = crncForm(request.POST)
        if form.is_valid():
            # Process the form data
            #my_field_data = form.cleaned_data['crname']
            form.save()
            return redirect('currency')
            #return JsonResponse({'success': True, 'message': 'Form submitted successfully'})
        #else:
            #return JsonResponse({'success': False, 'message': 'All Fields must fill !'})
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


#del currency
def del_currency(request):
    if request.method == 'POST':
        id = request.POST['crid']
        print(id)
        currency = crnc.objects.get(crid=id)
        currency.delete()
        return JsonResponse({'success': True, 'message': 'delete ok !'})

#currency search
def curr_ser2(request):
    if 'term' in request.GET:
        h = request.GET['term']
        #print(h)
        fields_to_search = ['crname', 'crsymbol','crdescription']
        # Build a Q object for each field
        queries = [Q(**{f'{field}__startswith': h}) for field in fields_to_search]
        # Combine the queries with OR condition
        search_query = queries.pop()
        for query in queries:
            search_query |= query
        # Perform the search using the Q object
        results = crnc.objects.filter(search_query)

        context = {
            'results': results,
            'query': query,
        }
        #print(results)
        #l = crnc.objects.filter(Q(crname__startswith=h) | Q(crsymbol__startswith=h))
        dot = []
        #print(l)
        s = list(results.values())
        #print(s)
        pac = []
        for j in s:
            pac.append(j.values())
        #print(pac)
        #pac=type(pac)
        print("list",pac)
        for i in results:
            #print(type(i))
            dot.append(i.crname)
        return JsonResponse(dot,safe = False)
    return redirect('/')

def curr_ser(request):
    if request.method == 'POST':
        d = request.POST['ser_name']
        fields_to_search = ['crname', 'crsymbol','crdescription']
        queries = [Q(**{f'{field}__startswith': d}) for field in fields_to_search]
        # Combine the queries with OR condition
        search_query = queries.pop()
        for query in queries:
            search_query |= query
        # Perform the search using the Q object
        print("ser",search_query)
        results = crnc.objects.filter(search_query)
        print(results)
        frm = crncForm()   
        model_meta = crnc._meta
        field_names = [field.verbose_name for field in model_meta.fields]
        return render(request,'currency.html',{'form': frm,'currency_info':results,'field_names': field_names})





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


def select_del(request):
    a=request.GET['select']
    print(a)
   
    return redirect('currency')


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
    
    
    