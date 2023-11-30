# urls.py

from django.urls import path
from . import views
app_name="event"

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.CreateUserView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
]
