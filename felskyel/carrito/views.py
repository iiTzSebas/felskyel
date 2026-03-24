from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Carrito, ItemCarrito
from appfel.models import Producto


# Create your views here.
@login_required 
def agregar_al_carrito(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    item, created = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    if not created:
        item.cantidad += 1
        item.save()
    return render(request, 'carrito/agregado.html', {'producto': producto})

@login_required
def ver_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.select_related('producto')
    return render(request, 'carrito/ver.html', {'carrito': carrito, 'items': items})

@login_required
def eliminar_del_carrito(request, item_id):
    item = ItemCarrito.objects.get(id=item_id)
    item.delete()
    return render(request, 'carrito/eliminado.html', {'item': item})

@login_required
def vaciar_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    carrito.items.all().delete()
    return render(request, 'carrito/vaciado.html')
@login_required
def sumar_cantidad(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id)
    item.cantidad += 1
    item.save()
    return redirect('carrito:ver_carrito')


@login_required
def restar_cantidad(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id)
    
    if item.cantidad > 1:
        item.cantidad -= 1
        item.save()
    else:
        item.delete()  # si queda en 0, se elimina

    return redirect('carrito:ver_carrito')