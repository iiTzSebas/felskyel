from django.db import models
from django.conf import settings
# Create your models here.
class Carrito(models.Model):
    """carrito asociado a un usuario"""
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Carrito de {self.usuario.username}"
    def total_items(self):
        """retorna el total de items en el carrito"""
        return sum(item.cantidad for item in self.items.all())
    def total_price(self):
        """retorna el precio total del carrito"""
        return sum(item.cantidad * item.producto.precio for item in self.items.all())