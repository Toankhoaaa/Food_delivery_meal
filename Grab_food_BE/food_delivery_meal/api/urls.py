from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('api/login', LoginView.as_view(), name='login'),
    path('api/register', CustomerRegistrationView.as_view(), name='register'),
]
