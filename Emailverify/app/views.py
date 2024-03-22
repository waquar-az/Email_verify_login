from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,LoginForm
from .models import Profile
from django.core.mail import send_mail
import uuid
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login,logout
# from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def Home(request):
    return render(request, 'home.html')

def About(request):
    return render(request, 'about.html')

def send_email_after_register(email,token):
    subject='verify account email'
    message=f'Hi click on link to verify your account http://127.0.0.1:8000/account-verify/{token}'
    from_email=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject=subject, message=message, from_email=from_email,recipient_list=recipient_list)

def SignUpView(request): 
    if request.method != 'POST':
        form = SignUpForm()
    else:
        form = SignUpForm(request.POST)
        if form.is_valid():           
            new_user=form.save()
            # print(new_user)
            uid=uuid.uuid4()
            # print(uid)
            pro_obj=Profile(user=new_user, token=uid)
            pro_obj.save()

            send_email_after_register(new_user.email, uid)
            messages.success(request,'Your account created succesfully,to verify account  check your mail')
            return redirect('sign-up')
    
    return render(request,'sign-up.html',{'form':form})

def Login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                profile = Profile.objects.get(user=user)
                if profile.verify:
                    login(request, user)
                    return redirect('home')  # Redirect to the appropriate URL after successful login
                else:
                    messages.info(request, 'Your account is not verified, please check your email')
                    return redirect('login')  # Redirect to the sign-in page
    else:
        form = LoginForm()
        
    return render(request, 'login.html', {'form': form})

def Logout(request):
    logout(request)
    return redirect('login')

def account_verify(request,token):    
    print(token)
    pf=Profile.objects.filter(token=token).first()
    print(pf)
    pf.verify=True
    pf.save()
    messages.success(request,'Your account has been verified,You can Login')
    return redirect('login')