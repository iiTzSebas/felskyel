from urllib import request
from productos.models import Producto   
from django.shortcuts import render

def lista_productos(request):
    # Aquí iría la lógica para obtener los productos desde la base de datos
    productos =  Producto.objects.all()
    # Reemplaza esto con tu consulta real a la base de datos
    contexto_catalogo = {'lista_productos': productos}
    return render(request, 'lista_productos.html', contexto_catalogo)