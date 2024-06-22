from django.urls import path
from . import views

urlpatterns = [
    path('product/', views.ProductListCreateAPIView.as_view(), name='product-get-post'),
    path('product/<int:pk>/', views.ProductDetailAPIView.as_view(), name='product-get-put'),
    path('admin/create/', views.AdminUserCreateView.as_view(), name='admin-add'),
    path('admin/update/<int:pk>/', views.AdminUserUpdateView.as_view(), name='admin-edit'),
    path('admin/delete/<int:pk>/', views.AdminUserDeleteView.as_view(), name='admin-delete'),
    path('admin/login/', views.LoginView.as_view(), name='admin-login'),
]