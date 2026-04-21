import pytest
from django.contrib.auth import get_user_model
from .models import Factura, ItemFactura
from productos.models import Producto
from carrito.models import Carrito # Asumiendo que existe el modelo
from django.urls import reverse
from decimal import Decimal

User = get_user_model()

@pytest.mark.django_db
def test_item_factura_subtotal():
    # 1. Preparación (Setup)
    usuario = User.objects.create_user(username="testuser", password="password123")
    factura = Factura.objects.create(usuario=usuario, total=0)
    producto = Producto.objects.create(
        nombre="Jabón Artesanal",
        precio=15000.00,
        stock=10,
        proveedor=usuario # Usando el usuario creado como proveedor para el test
    )
    
    item = ItemFactura.objects.create(factura=factura, producto=producto, cantidad=3, precio=producto.precio)
    
    # 2. Acción y Verificación (Assert)
    assert item.subtotal() == Decimal('45000.00')

@pytest.mark.django_db
def test_pago_exitoso_disminuye_stock(client):
    """Verifica que al procesar un pago exitoso, el stock del producto disminuya."""
    # 1. Setup
    password = "password123"
    usuario = User.objects.create_user(username="comprador", password=password, email="comprador@test.com")
    proveedor = User.objects.create_user(username="proveedor", password=password, user_type='proveedor', email="proveedor@test.com")
    
    producto = Producto.objects.create(
        nombre="Producto Test",
        precio=100.00,
        stock=10,
        disponible=True,
        proveedor=proveedor
    )
    
    # Simulamos el carrito (esto depende de cómo esté implementado tu modelo Carrito)
    carrito, _ = Carrito.objects.get_or_create(usuario=usuario)
    from carrito.models import ItemCarrito # Asumiendo nombre estándar
    ItemCarrito.objects.create(carrito=carrito, producto=producto, cantidad=3)
    
    client.login(username="comprador", password=password)
    
    # 2. Acción: Llamamos a la vista de éxito
    response = client.get(reverse('factura:exito'))
    
    # 3. Verificación
    producto.refresh_from_db()
    assert producto.stock == 7 # 10 iniciales - 3 comprados