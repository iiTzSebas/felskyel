from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, LoginForm
from .models import Usuario, ProviderApplication, ProviderProfile
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def reggistro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('user_type') == Usuario.PROVEEDOR:
                return redirect('solicitud_proveedor')
            usuario = form.save()
            login(request, usuario)
            messages.success(request, f"¡Bienvenido {usuario.username}! Tu cuenta ha sido creada exitosamente.")
            return redirect('inicio')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/reggistro.html', {'form': form})

def solicitud_proveedor_view(request):
    if request.method == 'POST':
        try:
            app = ProviderApplication.objects.create(
                nombre_completo=request.POST.get('nombre_completo'),
                nombre_negocio=request.POST.get('nombre_negocio'),
                email=request.POST.get('email'),
                telefono=request.POST.get('telefono'),
                domicilio=request.POST.get('domicilio'),
                documento_identidad=request.FILES.get('documento_identidad'),
                certificado_productos=request.FILES.get('certificado_productos'),
                registro_marca=request.FILES.get('registro_marca'),
                listado_productos=request.POST.get('listado_productos'),
                origen_productos=request.POST.get('origen_productos'),
            )
            
            # Notificar al admin
            send_mail(
                'Nueva Solicitud de Proveedor',
                f'El negocio {app.nombre_negocio} ha enviado una solicitud.',
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
            )
            
            messages.success(request, "Tu solicitud ha sido enviada. Revisaremos tus datos pronto.")
            return redirect('inicio')
        except Exception as e:
            messages.error(request, f"Error al enviar la solicitud: {e}")
            
    return render(request, 'solicitud-para-registro.html')

@login_required
def mi_perfil_view(request):
    if request.user.user_type == Usuario.PROVEEDOR:
        try:
            perfil = request.user.perfil_proveedor
            # Cambiamos a la plantilla que solicitas. 
            # Asegúrate de que el archivo se llame panel-control.html 
            # y esté en la carpeta templates/panel_control/
            return render(request, 'panel_control/panel-control.html', {'perfil': perfil})
        except ProviderProfile.DoesNotExist:
            messages.warning(request, "Tu perfil de proveedor aún no está configurado.")
            return redirect('inicio')
    else:
        return render(request, 'usuarios/p.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect('inicio')
        else:
            # mostrar errores generales para la consola debug
            print(form.errors)
            messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def p_view(request):
    # Redirigimos para que si entras por /p/ te mande a la lógica de perfiles corregida
    return redirect('mi_perfil')
