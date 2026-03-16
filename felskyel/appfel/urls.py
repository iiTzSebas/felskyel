from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='inicio'),
    path('shop/', views.shop, name='Tienda'),
    path('perfil/', views.perfil, name='perfil'),
    path('registro/', views.registro, name='registro'),
    path('contactos-proveedor/', views.contacto, name='contacto'),
    path('prueba2/', views.prueba2, name='prueba2'),
    path('prueba3/', views.prueba3, name='prueba3'),
    path('solicitud-proveedor/', views.solicitud_proveedor, name='solicitud_proveedor'),
    path('terminos-y-condiciones/', views.terminos_y_condiciones, name='terminos_y_condiciones'),
    path('panel-control/', views.panel, name='panel'),
    path('perfil_contacto/', views.perfil_contacto, name='perfil_contacto'),
    path('admin_productos/', views.admin_productos, name='admin_productos'),
    path('password_reset_request/', views.password_reset_request, name='password_reset_request'),
    path('password_reset_done/', views.password_reset_done, name='password_reset_done'),
    path('password_reset_complete/', views.password_reset_complete, name='password_reset_complete'),
    path('password_reset_confirm/', views.password_reset_confirm, name='password_reset_confirm'),
]
