from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

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
                return render(request, 'admin.html')
            
        else:
            # Handle invalid login credentials
            return render(request, 'admin/login.html', {'error_message': 'Invalid credentials'})

    return render(request, 'admin/login.html')
