from django.urls import path

from cart import views

app_name = 'cart'

urlpatterns = [
    path('cart-detail/', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.adding_to_cart, name='adding_to_cart'),
    path('remove/<int:product_id>/', views.remove_product_from_cart,
         name='remove_product_from_cart'),
]
