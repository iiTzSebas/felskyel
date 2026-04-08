from django.shortcuts import render
from productos.models import Producto
from django.db.models import Q

def buscar(request):
    query = request.GET.get('q')
    resultados = []
    if query:
        # Realiza la búsqueda en el nombre y la descripción del producto
        resultados = Producto.objects.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        ).distinct()
    return render(request, 'buscar/buscar.html', {'resultados': resultados, 'query': query})
