from django.urls import path
from registration import views

urlpatterns = [
    path('register/', views.register_request),
    path('login/', views.login_request),
    path('logout/', views.logout_request),
]
