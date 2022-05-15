from multiprocessing import context
from django.shortcuts import redirect, render
from django.views.decorators.cache import cache_control
from django.contrib import auth , messages
from django.contrib.auth.models import User

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_dashboard(request):
    if request.session.has_key('admin_session_key'):
        users = User.objects.all()
        context = {
            'users' : users,
        }
        return render(request, 'admin_dashboard.html',context)
    else:
        return redirect(admin_login)  

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_login(request):
    if request.session.has_key('admin_session_key'):
        return render(request, 'admin_dashboard.html')
    else:
        if request.method == 'POST':
            name = request.POST['name']
            password = request.POST['pass']
            admin = auth.authenticate(username = name, password = password)
            if admin is not None:
                if admin.is_superuser:
                    auth.login(request,admin)
                    request.session['admin_session_key'] = True
                    return redirect(admin_dashboard)
                else:
                    messages.error(request, 'You are not a Superadmin!')    
                    return render(request, 'admin_login.html') 
            else:
                messages.error(request, 'Invalid Credentials!')    
                return render(request, 'admin_login.html')            
        else:    
            return render(request, 'admin_login.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_logout(request):
    if request.session.has_key('admin_session_key'):
        del request.session['session_key']
        messages.success(request, "You'r logged out!")  
        return redirect(admin_login)
    else:
        return render(request,'admin_login.html')             
