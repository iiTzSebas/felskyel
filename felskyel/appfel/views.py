from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from usuarios.models import ProviderProfile # Importante importar el modelo correcto


# Create your views here.

def index(request):
    proveedores = ProviderProfile.objects.all()
    return render (request, 'index.html', {'proveedores': proveedores})

def detalle_proveedor(request, pk):
    # Buscamos el proveedor por su Primary Key (ID)
    proveedor = get_object_or_404(ProviderProfile, pk=pk)
    # Retornamos una nueva plantilla que crearemos a continuación
    return render(request, 'Contactos-proveedor/perfil_publico_proveedor.html', {'proveedor': proveedor})

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

@login_required
def perfil_contacto(request):
    # Intentamos obtener el perfil del proveedor logueado
    perfil = get_object_or_404(ProviderProfile, user=request.user)

    if request.method == 'POST':
        # Actualizamos los campos con lo que viene del formulario
        perfil.nombre_publico = request.POST.get('nombre_publico')
        perfil.descripcion = request.POST.get('descripcion')
        perfil.estado = request.POST.get('estado')
        perfil.color_fondo = request.POST.get('color_fondo')
        perfil.whatsapp = request.POST.get('whatsapp')
        perfil.instagram = request.POST.get('instagram')
        perfil.facebook = request.POST.get('facebook')
        perfil.telegram = request.POST.get('telegram')
        perfil.tiktok = request.POST.get('tiktok')

        # Manejo de la foto de perfil
        if request.FILES.get('foto_perfil'):
            perfil.foto_perfil = request.FILES.get('foto_perfil')

        perfil.save()
        messages.success(request, "¡Tu perfil público ha sido actualizado con éxito!")
        return redirect('perfil_contacto')

    # Si es un GET, simplemente mostramos el formulario con los datos actuales
    return render(request, 'panel_control/perfil_contacto.html', {'perfil': perfil})

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