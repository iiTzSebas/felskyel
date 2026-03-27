from productos.models import Producto   
from django.shortcuts import render, get_object_or_404

def lista_productos(request):
    # Aquí iría la lógica para obtener los productos desde la base de datos
    productos =  Producto.objects.all()
    # Reemplaza esto con tu consulta real a la base de datos
    contexto_catalogo = {'lista_productos': productos}
    return render(request, 'lista_productos.html', contexto_catalogo)

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'detalle_producto.html', {'producto': producto})