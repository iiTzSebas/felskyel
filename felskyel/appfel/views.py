from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from usuarios.models import ProviderProfile, Cita # Importante importar el modelo correcto


# Create your views here.

def index(request):
    # Solo mostramos proveedores que han marcado su perfil como activo
    proveedores = ProviderProfile.objects.filter(estado='activa')
    return render (request, 'index.html', {'proveedores': proveedores})

def detalle_proveedor(request, pk):
    # Buscamos el proveedor por su Primary Key (ID)
    proveedor = get_object_or_404(ProviderProfile, pk=pk)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para contactar al proveedor.")
            return redirect('login')

        # Crear la cita
        Cita.objects.create(
            cliente=request.user,
            proveedor=proveedor,
            nombre=request.POST.get('nombre'),
            apellido=request.POST.get('apellido'),
            email=request.POST.get('email'),
            telefono=request.POST.get('telefono'),
            direccion=request.POST.get('direccion'),
            mensaje=request.POST.get('mensaje'),
            fecha=request.POST.get('fecha') or None,
            hora=request.POST.get('hora') or None,
        )
        messages.success(request, f"Tu solicitud ha sido enviada a {proveedor.nombre_publico}. Te contactarán pronto.")
        return redirect('detalle_proveedor', pk=pk)

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
def cita(request):
    if request.user.user_type != 'proveedor':
        return redirect('inicio')
    
    # Obtenemos las citas que pertenecen al perfil del proveedor logueado
    perfil = get_object_or_404(ProviderProfile, user=request.user)
    citas = Cita.objects.filter(proveedor=perfil).order_by('-creada_en')
    
    return render(request, 'panel_control/cita-cliente.html', {'citas': citas})

@login_required
def gestionar_cita(request, cita_id, accion):
    perfil = get_object_or_404(ProviderProfile, user=request.user)
    cita_obj = get_object_or_404(Cita, id=cita_id, proveedor=perfil)
    
    if accion == 'aceptar':
        cita_obj.estado = 'aceptada'
        cita_obj.save()
        messages.success(request, f"La cita ha sido aceptada.")
    elif accion == 'rechazar':
        cita_obj.estado = 'rechazada'
        cita_obj.save()
        messages.success(request, f"La cita ha sido rechazada.")

    return redirect('cita')

@login_required
def eliminar_cita(request, cita_id):
    if request.user.user_type != 'proveedor':
        return redirect('inicio')
    
    perfil = get_object_or_404(ProviderProfile, user=request.user)
    # Buscamos la cita asegurando que pertenezca al proveedor logueado
    cita_obj = get_object_or_404(Cita, id=cita_id, proveedor=perfil)
    
    cita_obj.delete()
    messages.success(request, "El registro de la cita ha sido eliminado del historial.")
    return redirect('cita')

@login_required
def perfil_contacto(request):
    # 1. Validación de seguridad primero: Solo proveedores pueden editar su perfil público
    if request.user.user_type != 'proveedor':
        messages.error(request, "Acceso denegado. Esta sección es solo para proveedores.")
        return redirect('inicio')

    # 2. Intentamos obtener el perfil del proveedor logueado
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

def crud (request):
    return render (request, 'crud/indexx.html')

def terminos_y_condiciones(request):
    return render(request, 'terminos_y_condiciones.html')

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