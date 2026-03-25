from django.db import models

# Create your models here.

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    descripcion = models.TextField()
    imagen = models.CharField(max_length=200, default= "default.png")



    def __str__(self):
        return self.nombre
