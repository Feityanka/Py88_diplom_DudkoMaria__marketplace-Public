from django.urls import include, path
from django_registration.backends.one_step.views import RegistrationView
#from django_registration.

urlpatterns = [
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', RegistrationView.as_view(succes_url='/profile/')),
]
