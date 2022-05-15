from multiprocessing import context
from operator import index
from django.shortcuts import render
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    if request.session.has_key('session_key'):
        user = request.user
        context = {
            'user' : user,
        }
        return render(request,'index.html', context)
                
    else:
        return render(request,'login.html')
