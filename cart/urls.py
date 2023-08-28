from django.urls import path, include
from cart import views

urlpatterns = [
    path('cart_detail/', views.cart_detail, name='cart_detail'),
    path('add/', views.cart_add, name='cart_add'),
    path('remove/', views.cart_remove, name='cart_remove'),
    ]
