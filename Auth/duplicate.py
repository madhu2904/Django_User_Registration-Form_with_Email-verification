from pyexpat.errors import messages
import uuid
from django.shortcuts import redirect, render
from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.contrib import admin
from Auth.models import Profile
from django.core.mail import *
from . import models
from django.http import HttpResponse


from authentication import settings


class NewForm(forms.Form):
   
    email = forms.EmailField(widget=forms.EmailInput,label=mark_safe('<br/>Email'))
    password = forms.CharField(widget=forms.PasswordInput,label=mark_safe('<br/>Password'))
    password_confirm = forms.CharField(widget=forms.PasswordInput,label=mark_safe('<br/>Confirm Password'))
    
class NewForm1(forms.Form):
    username=forms.CharField(label=mark_safe('username'))
    email = forms.EmailField(widget=forms.EmailInput,label=mark_safe('<br/>Email'))
    password = forms.CharField(widget=forms.PasswordInput,label=mark_safe('<br/>Password'))
    password_confirm = forms.CharField(widget=forms.PasswordInput,label=mark_safe('<br/>Confirm Password'))
    

def index(request):
    return render(request,'login.html',{'forms':NewForm()})

def home(request):
    return render(request, 'index.html')


def register(request):
    if request.method == "POST":
        form = NewForm1(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username is already taken.')
                    return redirect('/register')

                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email is already taken.')
                    return redirect('/register')

                user_obj = User.objects.create(username=username, email=email)
                user_obj.set_password(password)
                user_obj.save()

                # Create and save profile object
                auth_token = str(uuid.uuid4())
                profile_obj = Profile.objects.create(user=user_obj, auth_token=auth_token)
                profile_obj.save()

                # Send email verification
                send_mail_after_registration(email, auth_token)

                return redirect('/token')  # Redirect to token verification page

            except Exception as e:
                print(e)
                messages.error(request, 'An error occurred during registration.')
                return redirect('/register')

    else:
        form = NewForm1()

    return render(request, 'register.html', {'forms': form})



def success(request):
    
    return render(request,'success.html')


def token(request):
    return render(request,'token.html')


def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
            return redirect('/login')  # Redirect to login page after successful verification
        else:
            return HttpResponse('Invalid token')  # Return an error message for invalid tokens
    except Exception as e:
        print(e)
        return HttpResponse('An error occurred')


def error_page(request):
    return render(request,'error.html')


def send_mail_after_registration(email,token):
    subject = "Your account needs to be verified"
    message = f'http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list)
        



# Create your views here.
