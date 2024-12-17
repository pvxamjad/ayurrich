from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User

def admin_login(request):
    admin = User.objects.get(username='amjad')
    last_log = admin.last_login
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_home')  # Redirect to the admin index or any other page
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html' ,{'last_log':last_log,})  # Adjust the path to your template


def admin_logout(request):
    logout(request) 
    return redirect('admin_login')