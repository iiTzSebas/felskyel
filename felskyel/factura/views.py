from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import stripe

from .models import Factura, ItemFactura
from carrito.models import Carrito
from productos.models import Producto

# 🔑 Configurar Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def crear_checkout(request):
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        items_db = carrito.items.all()
    except Carrito.DoesNotExist:
        return redirect('carrito:ver_carrito')

    if not items_db.exists():
        return redirect('carrito:ver_carrito')

    try:
        line_items = []
        for item in items_db:
            # Convertimos el precio a centavos para Stripe
            unidad_centavos = int(float(item.producto.precio) * 100)
            
            line_items.append({
                'price_data': {
                    'currency': 'cop',
                    'product_data': {'name': item.producto.nombre},
                    'unit_amount': unidad_centavos,
                },
                'quantity': item.cantidad,
            })

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='http://127.0.0.1:8000/factura/exito/',
            cancel_url='http://127.0.0.1:8000/factura/cancelado/',
        )
        
        return redirect(session.url)

    except stripe.error.StripeError as e:
        return HttpResponse(f"Error de Stripe: {e.user_message}")
    except Exception as e:
        return HttpResponse(f"Error inesperado: {str(e)}")

@login_required
def pago_exitoso(request):
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        items_db = carrito.items.all()
    except Carrito.DoesNotExist:
        return redirect('productos:lista_productos')

    if not items_db.exists():
        return redirect('productos:lista_productos')

    # 1. Crear la Factura
    factura = Factura.objects.create(
        usuario=request.user,
        pagada=True 
    )

    total = 0
    for item in items_db:
        ItemFactura.objects.create(
            factura=factura,
            producto=item.producto,
            cantidad=item.cantidad,
            precio=item.producto.precio
        )
        total += item.producto.precio * item.cantidad

    factura.total = total
    factura.save()

    # 2. Limpiar el carrito de la base de datos
    items_db.delete() 

    return redirect('factura:factura_detalle', factura_id=factura.id)

@login_required
def pago_cancelado(request):
    """Esta es la función que te faltaba y causaba el error"""
    return render(request, 'factura/cancelado.html')

@login_required
def factura_detalle(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    return render(request, 'factura/factura.html', {'factura': factura})