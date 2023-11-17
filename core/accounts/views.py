from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignUpForm
from .models import UserProfile

# def index(request):
#     return render(request, 'ecomm/index.html', {})

def signupView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(
                user = user,
            )
            return redirect('../login')
    
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {"form" : form})
        

def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
 
        if user is not None:
            login(request,user)
            return redirect('../../')
        else:
            messages.error(request, "Invalid Username or Password (try again) ")
    
    form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form':form})

def logoutView(request):
    logout(request)
    messages.info(request, "You have successfully logged out")
    return redirect("home")