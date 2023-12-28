from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
#from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from .form import *
from django.db.models.query_utils import Q
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required


def Login(request): 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_det = authenticate(request, username=username, password=password)
        
        if user_det is not None:
            user = get_object_or_404(User, username=username)
            login(request, user_det)
            if user.is_superuser:
                # Explicitly set the session to save the changes
               # request.session.save()
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
@login_required(login_url='/')
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
def del_currency_js(request):
    if request.method == 'POST':
        id = request.POST['crid']
        print(id)
        currency = crnc.objects.get(crid=id)
        currency.delete()
        return JsonResponse({'success': True, 'message': 'delete ok !'})

#delete currency
def del_currency(request,id):
    currency = crnc.objects.filter(pk=id)
    currency.delete()
    return redirect('currency')


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

        page=Paginator(results,5)
        page_list=request.GET.get('page')
        page=page.get_page(page_list)
        print(page)
        return render(request,'currency.html',{'form': frm,'currency_info':page,'field_names': field_names})







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
    if request.method == 'POST':
        frm = DocumentForm(request.POST)
        if frm.is_valid:
            frm.save()
            return redirect('document')
    else:
        frm = DocumentForm()
    model_meta = DocumentsRequired._meta
    field_names = [field.verbose_name for field in model_meta.fields]   
    document_info=DocumentsRequired.objects.all()
    print(document_info)
    return render(request,'document.html',{'form': frm,'document_info':document_info,'field_names': field_names})
    

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

#taxmaster

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
    tax_info=txmst.objects.all()
    return render(request,'taxmaster.html',{'form': frm,'tax_info':tax_info,'field_names': field_names})

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
    taxdetails=txdet.objects.all()
    return render(request,'taxdetails.html',{'form': frm,'taxdetails':taxdetails,'field_names': field_names})


def Logout(request):
    logout(request)
    return redirect('/')

# def crncform(request):
#     if request.method == 'POST':
#         frm = crncForm(request.POST)
        
#         if frm.is_valid:
#             frm.save()
#             return redirect('success_url')
#     else:
#         frm = crncForm()
        
#     return render(request, 'currency.html', {'form': frm})




    
    
 

def sample(request):
    return render(request,'page_js.html')

from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render


def paginated_and_filtered_data(request):
    page_number = request.GET.get('page', 1)
    items_per_page = 5  # Set the number of items per page

    queryset = crnc.objects.all()

    # Filter by name if a search term is provided
    search_term = request.GET.get('search', '')
    print(search_term)
    if search_term:
        print("if iiii")
        queryset = queryset.filter(crname__icontains=search_term)
        print(queryset)
    paginator = Paginator(queryset, items_per_page)

    try:
        current_page = paginator.page(page_number)
    except EmptyPage:
        return JsonResponse({'error': 'Invalid page number'})

    data = [{'crid':item.crid,'name': item.crname, 'symbol': item.crsymbol, 'description': item.crdescription,'status':item.crstatus,'usrid':item.usrid,'date':item.dtupdatd } for item in current_page.object_list]

    return JsonResponse({'data': data, 'total_pages': paginator.num_pages})

