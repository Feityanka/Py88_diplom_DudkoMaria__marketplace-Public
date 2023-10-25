from django.urls import path
from coupons import views

urlpatterns = [
    path('apply_coupon/', views.coupon_apply),
]
