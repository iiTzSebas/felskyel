from django.http import HttpResponse

from django.shortcuts import render

# Create your views here.

def prueba(request):
    return HttpResponse("Prueba pantalla")

def index(request):
    return render (request, 'index.html')

def shop(request):
    return render (request, 'shop.html')

def perfil(request):
    return render (request, 'perfil.html')

def registro(request):
    return render (request, 'registro.html')

def contacto(request):
    return render (request, 'contactos-proveedor/contacto.html')

def prueba2(request):
    return render (request, 'contactos-proveedor/prueba2.html')

def prueba3(request):
    return render (request, 'contactos-proveedor/prueba3.html')

def panel(request):
    return render (request, 'panel_control/panel-control.html')

def perfil_contacto(request):
    return render (request, 'panel_control/perfil_contacto.html')

def admin_productos(request):
    return render (request, 'panel_control/admin_productos.html')

def password_reset_request(request):
    return render (request, 'rest_passw/password_reset_request.html')

def password_reset_done(request):
    return render (request, 'rest_passw/password_reset_done.html')

def password_reset_confirm(request):
    return render (request, 'rest_passw/password_reset_confirm.html')

def password_reset_complete(request):
    return render (request, 'rest_passw/password_reset_complete.html')


def solicitud_proveedor(request):
    if request.method == 'POST':
        # Aquí iría la lógica para guardar los datos del formulario
        return HttpResponse("Solicitud recibida correctamente.")
    return render(request, 'solicitud-para-registro.html')

def terminos_y_condiciones(request):
    return HttpResponse("<h1>Términos y Condiciones</h1><p>Aquí va el contenido legal de tu sitio.</p>")
