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
path('event_list/',views.EventListView.as_view(), name='event_list'),
path('events/<int:event_id>/', views.EventDetailView.as_view(), name='event_detail'),
path('events/<int:event_id>/update/', views.EventUpdateView.as_view(), name='event_update'),
path('events/<int:event_id>/delete/', views.EventDeleteView.as_view(), name='event_delete'),

]
