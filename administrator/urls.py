# urls.py

from django.urls import path
from . import views
app_name="administrator"

urlpatterns = [
path('',views.HomeView.as_view(),name="dash_home"),
path('create_admin',views.CreateAdminView.as_view(),name="create_admin"),
path('login',views.LoginView.as_view(),name="login"),
path('change_password',views.ChangePasswordView.as_view(),name="change_password"),
path('logout/',views.LogoutView.as_view(), name='logout'),
path('create_event/',views.CreateEventView.as_view(), name='create_event'),
path('create_category/',views.CreateCategoryView.as_view(), name='create_category'),

]
