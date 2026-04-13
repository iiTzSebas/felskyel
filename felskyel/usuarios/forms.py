from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . models import Usuario
from django.core.exceptions import ValidationError

class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('user_type', 'username', 'email', 'es_mayor_edad')

    def clean_es_mayor_edad(self):
        es_mayor = self.cleaned_data.get('es_mayor_edad')
        if es_mayor is not True:
            raise ValidationError("Debes ser mayor de 18 años para registrarte.")
        return es_mayor

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Validación para evitar que el nombre sea puramente numérico
        if username and username.isdigit():
            raise ValidationError("El nombre de usuario no puede estar compuesto solo por números. Por favor, incluye letras.")
        return username

class LoginForm(AuthenticationForm):
    # NO HACE FALTA META
    pass