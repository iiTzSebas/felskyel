from django.urls import path
from . import views

app_name = 'carrito'

urlpatterns = [
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('', views.ver_carrito, name='ver_carrito'),
    path('eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('sumar/<int:item_id>/', views.sumar_cantidad, name='sumar_cantidad'),
    path('restar/<int:item_id>/', views.restar_cantidad, name='restar_cantidad'),
]