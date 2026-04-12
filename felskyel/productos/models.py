from django.db import models
from django.conf import settings
from django.templatetags.static import static

# Create your models here.

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    descripcion = models.TextField()
    stock = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='proveedores/imagenes/', null=True, blank=True)
    disponible = models.BooleanField(default=True)
    proveedor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mis_productos')

    @property
    def imagen_url(self):
        if self.imagen and hasattr(self.imagen, 'url'):
            return self.imagen.url
        return static('appfel/img/default.png')

    def __str__(self):
        return self.nombre
    
    def delete(self, using=None, keep_parents=False):
        if self.imagen:
            self.imagen.delete(save=False)
        super().delete()

class Comentario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='comentarios', null=True, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    calificacion = models.IntegerField(default=5)
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        destino = self.producto.nombre if self.producto else "General"
        return f"Comentario de {self.usuario.username} en {destino}"
