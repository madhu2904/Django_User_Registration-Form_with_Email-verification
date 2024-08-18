from pyexpat.errors import messages
import uuid
from django.shortcuts import redirect, render
from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.contrib import admin
from Auth.models import Profile
from django.core.mail import *


from authentication import settings


class NewForm(forms.Form):
   
    email = forms.EmailField(label=mark_safe('<br/>Email'))
    password = forms.CharField(widget=forms.PasswordInput,label=mark_safe('<br/>Password'))
    password_confirm = forms.CharField(widget=forms.PasswordInput,label=mark_safe('<br/>Confirm Password'))
    
class NewForm1(forms.Form):
    username=forms.CharField(label=mark_safe('userame'))
    email = forms.EmailField(label=mark_safe('<br/>Email'))
    password = forms.CharField(widget=forms.PasswordInput,label=mark_safe('<br/>Password'))
    password_confirm = forms.CharField(widget=forms.PasswordInput,label=mark_safe('<br/>Confirm Password'))
    

def index(request):
    return render(request,'Auth/login.html',{'forms':NewForm()})
def register(request):
        
        if request.method == 'POST' :
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')

        try:
            if User.objects.filter(username = username).first():
              #messages.success(request,'Username is taken.')
              return redirect('/register')
        
            elif User.objects.filter(email = email).first():
              #messages.success(request, 'Email is taken')
              return redirect('/register')
        
            user_obj = User.objects.create(username=username, email=email)
            user_obj.set_password(password)

            profile_obj = Profile.objects.create(user = user_obj , token = str(uuid.uuid4))
            profile_obj.save()

            return redirect('/token')

        except Exception as e:
            print(e)
        return render(request,'Auth/register.html',{'forms':NewForm1()})
def success(request):
    
    return render(request,'Auth/success.html')
def token(request):
    return render(request,'Auth/token.html')

def verify(request,auth_token):
    try:
        profile_obj=Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            profile_obj.is_verified=True
            profile_obj.save()
            messages.success(request,'You account is successfully verified')
            return redirect('/login')
        else:
            return redirect('error/')
    except Exception as e:
        print(e)

def error_page(request):
    return render(request,'error.html')
def send_mail_after_registration(email,token):
    subject = "Your account needs to be verified"
    message = f'http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list)