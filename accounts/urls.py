from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.register,name='login'),
    path('logout/',views.register,name='logout'),
]
