from django.urls import path
from user_profile.views import ShowProfilePageView, CreateProfilePageView

urlpatterns = [
    path('user_profile/', ShowProfilePageView.as_view(template_name='user_profile/user_profile.html'),
         name='user_profile'),
    path('create_profile_page/', CreateProfilePageView.as_view(template_name='user_profile/create_profile.html'),
         name='create_user_profile'),
]
