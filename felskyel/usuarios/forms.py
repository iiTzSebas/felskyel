from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . models import Usuario

class RegistroForm(UserCreationForm):
    class meta:
        model = Usuario
        fields = ['username', 'emaail', 'password1', 'password2', ]

class LoginForm(AuthenticationForm):
    # NO HACE FALTA META
    pass