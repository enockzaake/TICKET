from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate

from .models import CustomUser

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email,password=password)
        if user:
            login(request,user)
            return redirect('/')
    return render(request,'login.html')
    
def user_logout(request):
    logout(request)
    return redirect('/')

def user_register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            pass
    

        return redirect('/') 
    return render(request,'register.html')
    