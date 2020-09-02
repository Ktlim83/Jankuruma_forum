from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

def login_page(request):
    context = {
        'users': User.objects.get_all_by_email()
    }
    return render(request, 'login_page.html', context)

def registration_page(request):
    context = {
    }
    return render(request,'registration_page.html', context)



def registration(request):
    errors = User.objects.validate(request.POST)
    if errors:
        for field, value in errors.items():
            messages.error(request, value, extra_tags='register')
        return redirect('/registration_page')

    new_user = User.objects.register(request.POST)
    request.session['user_id'] = new_user.id
    messages.success(request, "You have successfully registered! Please sign in!", extra_tags='signup')
    return redirect('/')

def login(request):
    result = User.objects.authenticate(request.POST['email'], request.POST['password'])
    if result == False:
        messages.error(request, "Invalid Email/Password", extra_tags='log_in')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
        messages.success(request, "You have successfully logged in!", extra_tags='success')
        return redirect('/vroom')
    return redirect('/')



def logout(request):
    messages.success(request, "You have successfully logged out!", extra_tags='logout')
    request.session.clear()
    return redirect('/')





