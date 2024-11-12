# cart/urls.py
from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),  # View cart
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),  # Add to cart
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),  # Remove from cart
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),  # Apply coupon view
    path('checkout/', views.checkout, name='checkout'),  # Checkout view
]
