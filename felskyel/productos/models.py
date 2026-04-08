from django.db import models
from django.conf import settings

# Create your models here.

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    descripcion = models.TextField()
    imagen = models.CharField(max_length=200, default= "default.png")

    def __str__(self):
        return self.nombre

class Comentario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='comentarios', null=True, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    calificacion = models.IntegerField(default=5)
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        destino = self.producto.nombre if self.producto else "General"
        return f"Comentario de {self.usuario.username} en {destino}"
