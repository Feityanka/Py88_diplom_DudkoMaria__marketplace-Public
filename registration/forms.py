from django_registration.forms import RegistrationForm
from django.contrib.auth.forms import UserCreationForm


class CustomRegistrationForm(RegistrationForm):
    class Meta(UserCreationForm.Meta):
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'first_name',
            'last_name',
        ]
