from django.http import HttpResponse

from django.shortcuts import render

# Create your views here.

def index(request):
    return render (request, 'index.html')

def shop(request):
    return render (request, 'shop.html')

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

def crud (request):
    return render (request, 'crud/indexx.html')

def manual (request):
    return render (request, 'manual_usuario.html')

def terminos_y_condiciones(request):
    return HttpResponse("<h1>Términos y Condiciones</h1><p>Aquí va el contenido legal de tu sitio.</p>")

def jabon_de_carbon(request):
    return render (request, 'jabon_de_carbon.html')

def protector_labios(request):
    return render (request, 'protector-labios.html')

def shampoo(request):
    return render (request, 'shampoo.html')

def gel_ducha(request):
    return render (request, 'gel-ducha.html')

def primer_catalogo(request):
    return render (request, 'primer-catalogo.html')

def crema_manos(request):
    return render (request, 'crema-manos.html')

def manual_usuario(request):
    return render(request, 'manual_usuario.html')
