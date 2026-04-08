from django.urls import include, path
from . import views
from usuarios import views as usuarios_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='inicio'),
    path('shop/', views.shop, name='Tienda'),
    path('contactos-proveedor/', views.contacto, name='contacto'),
    
    path('solicitud-para-registro/', usuarios_views.solicitud_proveedor_view, name='solicitud_proveedor'),
    
    path('prueba2/', views.prueba2, name='prueba2'),
    path('prueba3/', views.prueba3, name='prueba3'),
    path('terminos-y-condiciones/', views.terminos_y_condiciones, name='terminos_y_condiciones'),
    path('panel-control/', views.panel, name='panel'),
    path('perfil_contacto/', views.perfil_contacto, name='perfil_contacto'),
    path('admin_productos/', views.admin_productos, name='admin_productos'),

    path('jabon-de-carbon/', views.jabon_de_carbon, name='jabon_de_carbon'),
    path('protector-labios/', views.protector_labios, name='protector_labios'),
    path('shampoo/', views.shampoo, name='shampoo'),
    path('gel-ducha/', views.gel_ducha, name='gel_ducha'),
    path('primer-catalogo/', views.primer_catalogo, name='primer_catalogo'),
    path('crema-manos/', views.crema_manos, name='crema_manos'),
    path('crud/', views.crud, name='crud'),
    path('manual/', views.manual, name='manual'),
    
        # 1. Formulario para ingresar el email
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='rest_passw/password_reset_request.html',
        email_template_name='rest_passw/password_reset_email.html', # Plantilla del contenido del correo
        success_url='/password_reset/done/'
    ), name='password_reset_request'),
    
        # 2. Mensaje de "Revisa tu correo"
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='rest_passw/password_reset_done.html'
    ), name='password_reset_done'), 
    
        # 3. El enlace que llega al correo (con token de seguridad)
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='rest_passw/password_reset_confirm.html',
        success_url='/reset/done/'
    ), name='password_reset_confirm'),
    
        # 4. Mensaje de éxito final
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='rest_passw/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    path('proveedor/<int:pk>/', views.detalle_proveedor, name='detalle_proveedor')
]
