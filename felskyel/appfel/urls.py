from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='inicio'),
    path('shop/', views.shop, name='Tienda'),
    path('perfil/', views.perfil, name='perfil'),
    path('registro/', views.registro, name='registro'),
    path('contacto/', views.contacto, name='contacto'),
    path('solicitud-proveedor/', views.solicitud_proveedor, name='solicitud_proveedor'),
    path('terminos-y-condiciones/', views.terminos_y_condiciones, name='terminos_y_condiciones'),
]
