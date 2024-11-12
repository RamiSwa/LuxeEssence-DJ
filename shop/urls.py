# shop/urls.py
from django.urls import path
from . import views

app_name = 'shop'  # Namespace for the shop app

urlpatterns = [
    path('', views.shop_view, name='shop_home'),  # Main shop page with all products
    path('category/<slug:slug>/', views.category_view, name='category'),  # Products filtered by category
    path('product/<slug:slug>/', views.product_detail_view, name='product_detail'),  # Detailed view for a single product
    path('product/<slug:slug>/add/', views.add_to_cart, name='add_to_cart'),  

]
