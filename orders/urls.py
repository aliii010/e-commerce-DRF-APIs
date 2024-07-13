from django.urls import path
from . import views

urlpatterns = [
  path('orders/', views.OrderView.as_view()),
  path('orders/<int:pk>/', views.SingleOrderView.as_view(), name='single-order'),
  path('order-items/', views.OrderItemView.as_view()),
  path('order-items/<int:pk>/', views.SingleOrderItemView.as_view(), name='single-order-item'),
]
