from django.shortcuts import render
from .form import *

# Create your views here.


def index(request):
    #  return redirect('/admin/')
    return render(request,'admin.html')

def currency(request):
    form = Currency_form()
    return render(request, 'currency.html', {'form': form})


def category(request):
    form = Category_form()
    return render(request,'category.html',{'form':form})

def country(request):
    form = Country_form()
    return render(request, 'country.html', {'form': form})
    
def document(request):
    form = Document_form()
    return render(request,'document.html',{'form': form})

def services(request):
    form = Service_form()
    return render(request,'services.html',{'form': form})