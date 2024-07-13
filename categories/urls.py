from django.urls import path
from . import views

urlpatterns = [
  path('categories/', views.CategoryView.as_view()),
  path('categories/<int:pk>/', views.CategoryView.as_view()),
  path('categories/<int:pk>/products/', views.CategoryProducts.as_view()),  
  path('categories/<int:pk>/variations/', views.CategoryVariations.as_view()),
  path('categories/<int:pk>/subcategories/', views.Subcategories.as_view()),
]
