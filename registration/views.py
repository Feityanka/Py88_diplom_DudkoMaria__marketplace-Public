from django.shortcuts import render

from django_registration.backends.one_step.views import RegistrationView

from registration.forms import CustomRegistrationForm


class CustomRegistrationView(RegistrationView):
    form_class = CustomRegistrationForm
