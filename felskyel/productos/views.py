from urllib import request

from django.shortcuts import render

def lista_productos(request):
    # Aquí iría la lógica para obtener los productos desde la base de datos
    productos = [
        {'nombre': 'jabon de carbon', 'precio': 10.99, 'descripcion': 'Jabón de carbón activado para una limpieza profunda.'},
        {'nombre': 'shampoo de avena', 'precio': 15.99, 'descripcion': 'Shampoo de avena para un cabello suave y saludable.'},
        {'nombre': 'crema hidratante', 'precio': 20.99, 'descripcion': 'Crema hidratante para una piel suave y tersa.'},
    ]  # Reemplaza esto con tu consulta real a la base de datos

    contexto_catalogo = {'lista_productos': productos}
    return render(request, 'lista_productos.html', contexto_catalogo)