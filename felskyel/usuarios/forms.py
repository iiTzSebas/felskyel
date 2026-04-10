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

class LoginForm(AuthenticationForm):
    # NO HACE FALTA META
    pass