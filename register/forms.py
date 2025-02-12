from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # Validacija za korisničko ime
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Korisničko ime već postoji. Molimo izaberite drugo.")
        return username

    # Email može biti dupliran, ali korisničko ime ne
    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email
