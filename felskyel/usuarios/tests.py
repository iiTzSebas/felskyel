import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.admin.sites import AdminSite
from unittest.mock import patch
from .models import Usuario, ProviderApplication, ProviderProfile
from .admin import ProviderApplicationAdmin

User = get_user_model()

@pytest.mark.django_db
@patch('requests.post')
def test_registro_usuario_cliente_exitoso(mock_post, client):
    """Prueba que un cliente puede registrarse aceptando términos y pasando el captcha."""
    # 1. Simulamos que Google responde 'success: True' al captcha
    mock_post.return_value.json.return_value = {'success': True}
    
    # 2. Datos del formulario (incluyendo lo que tu vista reggistro_view pide)
    url = reverse('reggistro') # Asegúrate de que este sea el nombre en tus urls.py
    data = {
        'username': 'juan123',
        'email': 'juan@example.com',
        'password1': 'Password123!',
        'password2': 'Password123!',
        'user_type': 'cliente',
        'es_mayor_edad': True,
        'aceptar_terminos': 'on', # Requerido por tu validación en views.py
        'g-recaptcha-response': 'token-ficticio' # Requerido por tu view
    }
    
    # 3. Ejecución
    response = client.post(url, data)
    
    # 4. Verificaciones
    # Tu vista hace redirect('inicio') tras un registro exitoso de cliente
    assert response.status_code == 302
    assert User.objects.filter(username='juan123').exists()
    assert response.url == reverse('inicio')

@pytest.mark.django_db
@patch('requests.post')
def test_registro_proveedor_redirecciona_a_solicitud(mock_post, client):
    """Verifica que al elegir 'proveedor' se redirija al formulario de solicitud."""
    # 1. Mock de captcha exitoso
    mock_post.return_value.json.return_value = {'success': True}
    
    url = reverse('reggistro')
    data = {
        'username': 'tienda_artesanal',
        'email': 'proveedor@test.com',
        'password1': 'Provee123!',
        'password2': 'Provee123!',
        'user_type': Usuario.PROVEEDOR, # 'proveedor'
        'es_mayor_edad': True,
        'aceptar_terminos': 'on',
        'g-recaptcha-response': 'token-ficticio'
    }
    
    # 2. Ejecución
    response = client.post(url, data)
    
    # 3. Verificación
    # Según tu views.py, si es proveedor redirige a 'solicitud_proveedor'
    assert response.status_code == 302
    assert response.url == reverse('solicitud_proveedor')
    # Verificamos que NO se haya creado el usuario aún (porque debe llenar la solicitud primero)
    assert not User.objects.filter(username='tienda_artesanal').exists()

@pytest.mark.django_db
def test_login_usuario_exitoso(client):
    """Prueba el flujo de inicio de sesión."""
    # 1. Crear el usuario en la DB de pruebas
    password = 'password123'
    user = User.objects.create_user(username='testuser', password=password)
    
    # 2. Intentar login
    url = reverse('login')
    response = client.post(url, {
        'username': 'testuser',
        'password': password
    })
    
    # 3. Verificación
    assert response.status_code == 302
    assert response.url == reverse('inicio')

@pytest.mark.django_db
def test_aprobacion_solicitud_proveedor_admin():
    """Prueba que la aprobación de una solicitud en el admin cree correctamente al usuario y su perfil."""
    # 1. Preparación: Creamos una solicitud de proveedor en la base de datos
    solicitud = ProviderApplication.objects.create(
        nombre_completo="Juan Admin Test",
        nombre_negocio="Artesanías del Sur",
        email="juan_admin@test.com",
        telefono="999888777",
        domicilio="Sede Central 1"
    )

    # Instanciamos el admin manualmente para ejecutar su lógica interna
    model_admin = ProviderApplicationAdmin(ProviderApplication, AdminSite())

    # 2. Acción: Llamamos al método privado que procesa la aprobación
    model_admin._procesar_aprobacion(solicitud)

    # 3. Verificaciones
    # Comprobamos que el usuario fue creado automáticamente con el rol de proveedor
    user = User.objects.get(email="juan_admin@test.com")
    assert user.user_type == Usuario.PROVEEDOR
    
    # Comprobamos que se generó su perfil de proveedor vinculado y activo
    perfil = ProviderProfile.objects.get(user=user)
    assert perfil.nombre_negocio == "Artesanías del Sur"
    assert perfil.estado == 'activa'

    # Verificamos que la solicitud original cambió de estado
    solicitud.refresh_from_db()
    assert solicitud.aprobada is True

    # Verificamos que se envió el correo de bienvenida (usando el outbox de Django)
    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == ["juan_admin@test.com"]

@pytest.mark.django_db
def test_mi_perfil_anonimo_redirige_login(client):
    """Verifica que un usuario no autenticado sea redirigido al login al intentar ver su perfil."""
    url = reverse('mi_perfil')
    response = client.get(url)
    assert response.status_code == 302
    assert "/login" in response.url

@pytest.mark.django_db
@patch('requests.post')
def test_enviar_solicitud_proveedor_exitoso(mock_post, client):
    """Prueba que un aspirante puede enviar su solicitud con documentos."""
    mock_post.return_value.json.return_value = {'success': True}
    
    # Simulamos archivos PDF/Imagen
    documento = SimpleUploadedFile("dni.pdf", b"contenido_archivo", content_type="application/pdf")
    
    url = reverse('solicitud_proveedor')
    data = {
        'nombre_completo': 'Carlos Proveedor',
        'nombre_negocio': 'EcoTienda',
        'email': 'carlos@ecotienda.com',
        'telefono': '123456789',
        'domicilio': 'Calle Falsa 123',
        'listado_productos': 'Jabones, Cremas',
        'origen_productos': 'Artesanal',
        'aceptar_terminos': 'on',
        'g-recaptcha-response': 'token-ficticio',
        'documento_identidad': documento
    }
    
    response = client.post(url, data)
    
    # Verificaciones
    assert response.status_code == 302
    assert ProviderApplication.objects.filter(email='carlos@ecotienda.com').exists()
    # Verificar que se notificó al admin por correo
    assert len(mail.outbox) == 1
    assert "Nueva Solicitud" in mail.outbox[0].subject

@pytest.mark.django_db
@patch('requests.post')
def test_registro_usuario_fallo_captcha(mock_post, client):
    """Verifica que el registro falle si el reCAPTCHA es inválido."""
    # Simulamos que Google responde que el captcha falló
    mock_post.return_value.json.return_value = {'success': False}
    
    url = reverse('reggistro')
    data = {
        'username': 'intento_fallido',
        'email': 'fallo@test.com',
        'password1': 'Pass123!',
        'password2': 'Pass123!',
        'user_type': 'cliente',
        'es_mayor_edad': True,
        'aceptar_terminos': 'on',
        'g-recaptcha-response': 'token-invalido'
    }
    
    response = client.post(url, data)
    
    # No debe haber redirección (302), sino recarga de página (200)
    assert response.status_code == 200
    # El usuario NO debe existir en la base de datos
    assert not User.objects.filter(username='intento_fallido').exists()
    # Verificamos que el mensaje de error específico se muestre
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert "Por favor, confirma que no eres un robot." in messages

@pytest.mark.django_db
@patch('requests.post')
def test_registro_usuario_sin_aceptar_terminos(mock_post, client):
    """Verifica que el registro falle si el usuario no marca el checkbox de términos."""
    mock_post.return_value.json.return_value = {'success': True}
    
    url = reverse('reggistro')
    data = {
        'username': 'rebelde_sin_terminos',
        'email': 'rebelde@test.com',
        'password1': 'Pass123!',
        'password2': 'Pass123!',
        'user_type': 'cliente',
        'es_mayor_edad': True,
        # Omitimos 'aceptar_terminos'
        'g-recaptcha-response': 'token-valido'
    }
    
    response = client.post(url, data)
    
    assert response.status_code == 200
    assert not User.objects.filter(username='rebelde_sin_terminos').exists()
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert "Debes aceptar los términos y condiciones para registrarte." in messages

@pytest.mark.django_db
@patch('requests.post')
def test_solicitud_proveedor_fallo_captcha(mock_post, client):
    """Verifica que la solicitud de proveedor no se guarde si el captcha falla."""
    mock_post.return_value.json.return_value = {'success': False}
    
    url = reverse('solicitud_proveedor')
    data = {'nombre_completo': 'Fallo Prov', 'g-recaptcha-response': 'test'}
    
    response = client.post(url, data)
    
    assert response.status_code == 200
    assert not ProviderApplication.objects.filter(nombre_completo='Fallo Prov').exists()
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert "CAPTCHA inválido. Intenta de nuevo." in messages