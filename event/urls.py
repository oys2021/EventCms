# urls.py

from django.urls import path
from . import views
app_name="event"

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.CreateUserView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('home', views.HomeView.as_view(), name='home_view'),
    path('event-details/<int:event_id>', views.EventDetailsView.as_view(), name='event-details'),
    path('register_event/<int:event_id>', views.RegisterEventView.as_view(), name='register_event'),
]
