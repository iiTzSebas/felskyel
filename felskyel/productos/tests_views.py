import pytest
from django.urls import reverse
from productos.models import Producto, Comentario
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_lista_productos_view(client):
    """Verifica que la página de productos cargue correctamente."""
    url = reverse('productos:lista_productos')
    response = client.get(url)
    
    assert response.status_code == 200
    assert "lista_productos.html" in [t.name for t in response.templates]

@pytest.mark.django_db
def test_detalle_producto_200(client):
    """Verifica que la página de detalle de un producto cargue correctamente."""
    proveedor = User.objects.create_user(username='p1', password='pw', user_type='proveedor')
    producto = Producto.objects.create(nombre="Test Product", precio=100, stock=5, proveedor=proveedor)
    
    url = reverse('productos:detalle', kwargs={'producto_id': producto.id})
    response = client.get(url)
    
    assert response.status_code == 200
    assert "Test Product" in response.content.decode()

@pytest.mark.django_db
def test_detalle_producto_404(client):
    """Verifica que un producto inexistente devuelva error 404."""
    # Intentamos acceder a un ID que no existe (999)
    url = reverse('productos:detalle', kwargs={'producto_id': 999})
    response = client.get(url)
    
    assert response.status_code == 404

@pytest.mark.django_db
def test_admin_productos_vista_carga_proveedor(client):
    """Verifica que el panel de administración cargue para un proveedor (Status 200)."""
    user = User.objects.create_user(username='proveedor_ok', password='password123', user_type='proveedor')
    client.login(username='proveedor_ok', password='password123')
    
    url = reverse('productos:admin_productos')
    response = client.get(url)
    
    assert response.status_code == 200

@pytest.mark.django_db
def test_crear_producto_proveedor_exitoso(client):
    """Verifica que un proveedor autenticado pueda crear un producto."""
    # 1. Preparación: Crear e iniciar sesión como proveedor
    password = 'password123'
    user = User.objects.create_user(username='proveedor_test', password=password, user_type='proveedor')
    client.login(username='proveedor_test', password=password)
    
    url = reverse('productos:admin_productos')
    data = {
        'nombre': 'Jabón Orgánico de Avena',
        'precio': 15000,
        'descripcion': 'Hecho a mano con ingredientes naturales',
        'stock': 20,
        'disponible': 'on'
    }
    
    # 2. Acción: Enviar la petición POST para crear el producto
    response = client.post(url, data)
    
    # 3. Verificación: Redirección al panel y existencia en base de datos
    assert response.status_code == 302
    assert response.url == reverse('productos:admin_productos')
    assert Producto.objects.filter(nombre='Jabón Orgánico de Avena', proveedor=user).exists()

@pytest.mark.django_db
def test_admin_productos_acceso_denegado_cliente(client):
    """Verifica que un cliente no tenga permiso para acceder a la gestión de productos."""
    # 1. Preparación: Crear e iniciar sesión como cliente
    password = 'password123'
    user = User.objects.create_user(username='cliente_test', password=password, user_type='cliente')
    client.login(username='cliente_test', password=password)
    
    url = reverse('productos:admin_productos')
    response = client.get(url)
    
    # 2. Verificación: Debe ser redirigido al inicio por falta de permisos
    assert response.status_code == 302
    assert response.url == reverse('inicio')

@pytest.mark.django_db
def test_crear_producto_invalido(client):
    """Verifica que no se cree un producto si faltan datos obligatorios."""
    user = User.objects.create_user(username='p_test', password='pw', user_type='proveedor')
    client.login(username='p_test', password='pw')
    
    url = reverse('productos:admin_productos')
    # Datos incompletos (sin nombre, que tu vista valida en 'if nombre and precio')
    data = {'precio': 15000}
    response = client.post(url, data)
    
    assert response.status_code == 200 
    assert Producto.objects.count() == 0

@pytest.mark.django_db
def test_eliminar_producto_ajeno_denegado(client):
    """Verifica que un proveedor no pueda eliminar productos de otro proveedor."""
    p1 = User.objects.create_user(username='p1', password='pw', user_type='proveedor')
    p2 = User.objects.create_user(username='p2', password='pw', user_type='proveedor')
    prod_p1 = Producto.objects.create(nombre="Prod P1", precio=100, proveedor=p1)
    
    client.login(username='p2', password='pw')
    url = reverse('productos:eliminar_producto', kwargs={'producto_id': prod_p1.id})
    response = client.get(url)
    
    # Tu vista usa get_object_or_404(..., proveedor=request.user), así que debe dar 404
    assert response.status_code == 404
    assert Producto.objects.filter(id=prod_p1.id).exists()

@pytest.mark.django_db
def test_admin_productos_anonimo_redirige_login(client):
    """Verifica que un usuario anónimo sea redirigido al login al intentar entrar al panel."""
    url = reverse('productos:admin_productos')
    response = client.get(url)
    assert response.status_code == 302
    assert "/login" in response.url

@pytest.mark.django_db
def test_editar_producto_ajeno_denegado(client):
    """Verifica que un proveedor no pueda acceder a la edición de productos de otros."""
    p1 = User.objects.create_user(username='p1', password='pw', user_type='proveedor')
    p2 = User.objects.create_user(username='p2', password='pw', user_type='proveedor')
    prod_p1 = Producto.objects.create(nombre="Prod P1", precio=100, proveedor=p1)
    
    client.login(username='p2', password='pw')
    url = reverse('productos:editar_producto', kwargs={'producto_id': prod_p1.id})
    response = client.get(url)
    
    assert response.status_code == 404

@pytest.mark.django_db
def test_actualizar_stock_acceso_denegado_cliente(client):
    """Verifica que un cliente no pueda actualizar stock de productos."""
    p1 = User.objects.create_user(username='p1', password='pw', user_type='proveedor')
    prod = Producto.objects.create(nombre="Prod", precio=100, proveedor=p1)
    
    User.objects.create_user(username='cliente_hacker', password='pw', user_type='cliente')
    client.login(username='cliente_hacker', password='pw')
    
    url = reverse('productos:actualizar_stock', kwargs={'producto_id': prod.id})
    response = client.post(url, {'cantidad_sumar': 10})
    
    assert response.status_code == 302
    assert response.url == reverse('inicio')

@pytest.mark.django_db
def test_crear_comentario_producto_autenticado(client):
    """Verifica que un usuario logueado pueda comentar en un producto."""
    user = User.objects.create_user(username='comentador', password='pw1')
    prov = User.objects.create_user(username='prov', password='pw2', user_type='proveedor')
    prod = Producto.objects.create(nombre="Prod", precio=100, proveedor=prov)
    
    client.login(username='comentador', password='pw1')
    url = reverse('productos:detalle', kwargs={'producto_id': prod.id})
    
    data = {
        'rating': 5,
        'comment': 'Excelente producto, muy recomendado.'
    }
    
    response = client.post(url, data)
    
    assert response.status_code == 302
    assert Comentario.objects.filter(producto=prod, usuario=user).exists()

@pytest.mark.django_db
def test_producto_stock_no_negativo():
    """Verifica que la base de datos proteja la integridad del stock (si se configuró el validador)."""
    from django.core.exceptions import ValidationError
    proveedor = User.objects.create_user(username='p_stock', password='pw', user_type='proveedor')
    
    # Si intentamos crear un producto con stock negativo
    with pytest.raises(Exception): # O ValidationError si usas validadores de Django
        Producto.objects.create(nombre="Malo", precio=10, stock=-1, proveedor=proveedor)