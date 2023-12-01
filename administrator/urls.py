# urls.py

from django.urls import path
from . import views
app_name="administrator"

urlpatterns = [
path('',views.HomeView.as_view(),name="dash_home"),
path('create_admin',views.CreateAdminView.as_view(),name="create_admin"),
path('login',views.LoginView.as_view(),name="login")
]
