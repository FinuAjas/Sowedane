from . import views
from django.urls import path


urlpatterns = [
    path('',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logoutuser/',views.logoutuser,name='logoutuser'),
    path('activate/<uidb64>/<token>',views.activate, name='activate'),
    path('edituserprofile/<int:id>',views.edituserprofile, name='edituserprofile'),
]