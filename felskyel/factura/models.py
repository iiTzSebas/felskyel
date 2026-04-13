from django.db import models
from productos.models import Producto
from django.conf import settings

class Factura(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Indica si el pago de Stripe se completó con éxito
    pagada = models.BooleanField(default=False)

    def __str__(self):
        return f"Factura {self.id} - {self.usuario.username}"


class ItemFactura(models.Model):
    factura = models.ForeignKey(Factura, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField() # Usamos Positive para evitar cantidades negativas
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"

    # Esta es la función que permite usar {{ item.subtotal }} en el HTML
    def subtotal(self):
        return self.cantidad * self.precio