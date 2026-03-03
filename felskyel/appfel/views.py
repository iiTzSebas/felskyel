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
    return render (request, 'prueba2.html')

def solicitud_proveedor(request):
    if request.method == 'POST':
        # Aquí iría la lógica para guardar los datos del formulario
        return HttpResponse("Solicitud recibida correctamente.")
    return render(request, 'solicitud-para-registro.html')

def terminos_y_condiciones(request):
    return HttpResponse("<h1>Términos y Condiciones</h1><p>Aquí va el contenido legal de tu sitio.</p>")
