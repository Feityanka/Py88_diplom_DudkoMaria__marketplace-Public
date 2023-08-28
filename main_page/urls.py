from django.urls import path, include
from main_page import views

urlpatterns = [
    path('', views.home, name='main_page'),
    path('authentication/', include('djoser.urls')),
    path('authentication/', include('djoser.urls.jwt')),
    ]
