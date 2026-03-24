from django.db import models
from django.conf import settings
from appfel.models import Producto

class Carrito(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

    def total_items(self):
        return sum(item.cantidad for item in self.items.all())

    def total_price(self):
        return sum(item.cantidad * item.producto.precio for item in self.items.all())


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey('appfel.Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)  # ✅ CORREGIDO

    class Meta:
        unique_together = ('carrito', 'producto')

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

    @property
    def subtotal(self):  # ✅ SOLO ESTE
        return self.cantidad * self.producto.precio