from django.shortcuts import render
from .forms import UserForm,UserProfileForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def register(req):
    
    is_registered = False
    
    if req.method == 'POST':
        user_form = UserForm(data=req.POST)
        profile_form = UserProfileForm(data=req.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user ## one to one relationship
            
            if 'profile_pfp' in req.FILES:
                profile.profile_pfp = req.FILES['profile_pfp']
            profile.save()
            is_registered = True
        else :
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
            
    return render(req,'basic_app/registration.html',{
        'user_form':user_form,
        'profile_form':profile_form,
        'is_registered':is_registered,
    })

def index(req):
    return render(req,'basic_app/index.html')


@login_required
def something_special(req):
    return HttpResponse('You are logged in, Nice !!!')
@login_required
def user_logout(req):
    logout(req)
    return HttpResponseRedirect(reverse('index'))


def user_login(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')
        
        user = authenticate(username=username,password=password)
        
        if user:
            if user.is_active:
                login(req,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                HttpResponse('Account not active')
        else:
            print('Someone tried to login and failed')
            print("Username: {} and password {}".format(username,password))
            return HttpResponse('Invalid Login details supplied')
    else:
        return render(req,'basic_app/login.html',{})