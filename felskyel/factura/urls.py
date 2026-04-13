from django.urls import path
from . import views

app_name = 'factura'

urlpatterns = [
    path('checkout/', views.crear_checkout, name='checkout'),
    path('exito/', views.pago_exitoso, name='exito'),
    path('cancelado/', views.pago_cancelado, name='cancelado'),
    path('factura/<int:factura_id>/', views.factura_detalle, name='factura_detalle'),
]