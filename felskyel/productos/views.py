from productos.models import Producto, Comentario
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Avg

def lista_productos(request):
    productos = Producto.objects.all()
    # Obtenemos los últimos 4 comentarios de cualquier producto para la sección general
    comentarios_generales = Comentario.objects.select_related('usuario', 'producto').all().order_by('-fecha')[:4]

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