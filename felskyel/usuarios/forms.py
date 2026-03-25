from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . models import Usuario

class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email']

class LoginForm(AuthenticationForm):
    # NO HACE FALTA META
    pass