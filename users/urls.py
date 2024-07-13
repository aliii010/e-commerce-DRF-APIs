from django.urls import path
from . import views

urlpatterns = [
  path('users/', views.ListUsers.as_view()),
  path('customers/', views.ListCustomers.as_view()),
  path('admins/', views.ListAdminUsers.as_view()),
]
