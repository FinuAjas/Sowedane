from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('home.urls')),
    path('login/',include('userauthentication.urls')),
    path('newadmin/',include('newadmin.urls')),
]
