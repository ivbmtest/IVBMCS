from django.shortcuts import render

# Create your views here.


def index(request):
    #  return redirect('/admin/')
    return render(request,'admin.html')

def currency(request):
    return render(request,'currency.html')


def category(request):
    return render(request,'category.html')

def country(request):
    return render(request,'country.html')

def document(request):
    return render(request,'document.html')

def services(request):
    return render(request,'services.html')