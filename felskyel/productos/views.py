from productos.models import Producto, Comentario
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Avg
from django.contrib.auth.decorators import login_required

@login_required
def admin_productos(request):
    # Corregimos la validación según el modelo Usuario (donde PROVEEDOR = 'proveedor')
    if request.user.user_type != 'proveedor':
        messages.error(request, "Acceso denegado. Solo proveedores pueden administrar productos.")
        return redirect('inicio')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        descripcion = request.POST.get('descripcion')
        imagen = request.FILES.get('imagen')
        # El stock se puede manejar como un booleano de disponibilidad
        disponible = request.POST.get('disponible') == 'on'

        if nombre and precio:
            Producto.objects.create(
                nombre=nombre,
                precio=precio,
                descripcion=descripcion,
                imagen=imagen,
                # Asegúrate de que el modelo Producto tenga el campo 'user' o 'proveedor'
                # proveedor=request.user 
            )
            messages.success(request, f"Producto '{nombre}' añadido correctamente.")
            return redirect('productos:admin_productos')

    productos_proveedor = Producto.objects.all() # Aquí podrías filtrar por proveedor en el futuro
    return render(request, 'panel_control/admin_productos.html', {'productos': productos_proveedor})

def lista_productos(request):
    productos = Producto.objects.all()
    # Filtramos para obtener solo comentarios que NO pertenecen a un producto (comentarios del sitio)
    comentarios_generales = Comentario.objects.filter(producto__isnull=True).select_related('usuario').order_by('-fecha')[:4]

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para dejar un comentario.")
            return redirect('login')
        
        texto = request.POST.get('texto', '').strip()
        
        if texto:
            Comentario.objects.create(
                usuario=request.user,
                texto=texto,
                # producto=None y calificacion=5 ya son los valores por defecto
                # definidos en el modelo, por lo que no es estrictamente
                # necesario pasarlos aquí si no cambian.
            )
            return redirect('productos:lista_productos')
        else:
            messages.warning(request, "El comentario no puede estar vacío.")

    contexto_catalogo = {
        'lista_productos': productos,
        'comentarios_generales': comentarios_generales
    }
    return render(request, 'lista_productos.html', contexto_catalogo)

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    comentarios = Comentario.objects.filter(producto=producto).order_by('-fecha')
    promedio = comentarios.aggregate(Avg('calificacion'))['calificacion__avg'] or 0

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para dejar un comentario.")
            return redirect('login') # Ajusta el nombre de tu URL de login
        
        calificacion = request.POST.get('rating', 5)
        texto = request.POST.get('comment', '').strip()
        
        if texto:
            Comentario.objects.create(
                producto=producto, 
                usuario=request.user, 
                calificacion=int(calificacion), 
                texto=texto
            )
            messages.success(request, "¡Gracias! Tu opinión ha sido enviada.")
        else:
            messages.warning(request, "El comentario no puede estar vacío.")
            
        return redirect('productos:detalle', producto_id=producto.id)

    # Obtenemos 4 productos aleatorios o diferentes al actual para la sección "Relacionados"
    related_products = Producto.objects.exclude(id=producto.id).order_by('?')[:4]

    contexto = {
        'producto': producto,
        'comentarios': comentarios,
        'promedio': round(promedio, 1),
        'total_comentarios': comentarios.count(),
        'related_products': related_products
    }
    return render(request, 'detalle_producto.html', contexto)

@login_required
def eliminar_producto(request, producto_id):
    if request.user.user_type == 'proveedor':
        producto = get_object_or_404(Producto, id=producto_id)
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f"Producto '{nombre}' eliminado.")
    return redirect('productos:admin_productos')