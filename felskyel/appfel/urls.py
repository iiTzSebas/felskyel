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
]
