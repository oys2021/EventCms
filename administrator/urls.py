# urls.py

from django.urls import path
from . import views
app_name="administrator"

urlpatterns = [
path('',views.HomeView.as_view(),name="dash_home")
]
