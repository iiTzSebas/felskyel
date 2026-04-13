import pytest
from django.contrib.auth import get_user_model
from .models import Factura, ItemFactura
from productos.models import Producto
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