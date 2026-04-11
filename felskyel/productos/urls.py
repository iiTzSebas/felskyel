from django.urls import path
from . import views

app_name = 'productos'


urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('<int:producto_id>/', views.detalle_producto, name='detalle'),
    path('admin_productos/', views.admin_productos, name='admin_productos'),
    path('eliminar_producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('comentarios-generales/', views.todos_los_comentarios_generales, name='todos_los_comentarios_generales'),
    path('editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),

]