from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class NewUserForm(forms.Form):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save_new_user(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
