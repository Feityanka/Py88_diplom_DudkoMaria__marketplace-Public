from django.urls import path, include
from main_page import views


app_name = 'main_page'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list,
         name='product_list_by_category'),
    path('<int:id>,/<slug:slug>/', views.product_detail,
         name='product_detail'),
    path('authentication/', include('djoser.urls')),
    path('authentication/', include('djoser.urls.jwt')),
]
