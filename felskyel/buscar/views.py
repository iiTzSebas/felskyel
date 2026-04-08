from django.shortcuts import render
from productos.models import Producto
from django.core.paginator import Paginator
from django.db.models import Q

def buscar(request):
    query = request.GET.get('q', '').strip()
    productos = Producto.objects.all()

    if query:
        # Palabras que no aportan a la búsqueda
        stopwords = ['de', 'la', 'el', 'y', 'a', 'en', 'para', 'con']

        # Filtrar palabras útiles
        palabras = [p for p in query.split() if p.lower() not in stopwords]

        filtros = Q()

        for palabra in palabras:
            filtros |= Q(nombre__icontains=palabra)
            filtros |= Q(descripcion__icontains=palabra)

        productos = productos.filter(filtros).distinct()

    # Paginación
    paginator = Paginator(productos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'buscar/buscar.html', {
        'page_obj': page_obj,
        'query': query
    })