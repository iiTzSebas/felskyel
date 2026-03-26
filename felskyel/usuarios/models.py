from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.
class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    
    # ... tus otros campos ...
    user_type = models.CharField(max_length=20, default='cliente')
    fecha_nacimiento = models.DateField(null=True, blank=True)

    #Evitar conflictos de reverse accessors
    groups = models.ManyToManyField(
        Group, 
        related_name='usuarios_set', #aqui cambia el related_name
        blank=True,
        help_text='Los grupos a los que pertenece el usuario.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        Permission, 
        related_name='usuarios_user_set', #aqui cambia el related_name
        blank=True,
        help_text='Permisos específicos para este usuario.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username
