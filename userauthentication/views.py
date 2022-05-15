from base64 import urlsafe_b64encode
from email.message import EmailMessage
from email.policy import default
import django
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from home.views import home
from django.contrib import messages, auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from . form import UserForm



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    if request.session.has_key('session_key'):
        return render(request,'index.html')
    else:
        if request.method == 'POST':
            name = request.POST['name']
            password = request.POST['pass']
            user = auth.authenticate(username = name, password = password)
            if user is not None:
                auth.login(request,user)
                request.session['session_key'] = True
                return render(request,'index.html')
            else:
                messages.error(request, 'Invalid login credentials.')
                return redirect(login)
        else:
            return render(request,'login.html')
        
     

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register(request):
    if request.session.has_key('session_key'):
        return render(request, 'index.html') 
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password =request.POST.get('pass')
            user = User.objects.create_user(username = username,first_name = first_name, last_name = last_name, email = email, password = password)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('account_verification_email.html', {
                'user': user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request, 'Thank You for registering! Please check your email to activate your account.')  
            return render(request, 'confirmemail.html')
        else:    
            return render(request, 'register.html')    

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError,OverflowError,User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True        
        user.save()
        messages.success(request, 'Congratulations! Your account is activated!')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link!')
        return redirect('register') 


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logoutuser(request):
    if request.session.has_key('session_key'):
        del request.session['session_key']
        messages.success(request, "You'r logged out!")  
        return redirect(login)
    else:
        return render(request,'login.html')  


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edituserprofile(request, id):
    if request.method == "POST":
        instance = get_object_or_404(User, id=id)
        form = UserForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            instance = get_object_or_404(User, id=id)
            form = UserForm(request.POST or None, instance=instance)
            context = {
                    'form' : form,
                    'user' : instance,
                    }
            return render(request, 'edituserprofile.html',context)
    else:
        instance = get_object_or_404(User, id=id)
        form = UserForm(request.POST or None, instance=instance)
        context = {
                'form'   : form,
                'user'   : instance,
                }
        return render(request, 'edituserprofile.html',context)                       

  
