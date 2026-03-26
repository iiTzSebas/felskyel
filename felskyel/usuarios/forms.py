from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . models import Usuario
from datetime import date
from django.core.exceptions import ValidationError

class RegistroForm(UserCreationForm):
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Fecha de Nacimiento"
    )

    class Meta:
        model = Usuario
        fields = ('user_type', 'username', 'email', 'fecha_nacimiento')

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get('fecha_nacimiento')
        today = date.today()
        edad = today.year - fecha.year - ((today.month, today.day) < (fecha.month, fecha.day))
        if edad < 18:
            raise ValidationError("Debes tener al menos 18 años para registrarte.")
        return fecha

class LoginForm(AuthenticationForm):
    # NO HACE FALTA META
    pass