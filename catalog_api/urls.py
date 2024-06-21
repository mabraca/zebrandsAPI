from django.urls import path
from . import views

urlpatterns = [
    path('product/list/', views.ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('product/<int:pk>/', views.ProductDetailAPIView.as_view(), name='product-detail'),
]