from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.
class Usuario(AbstractUser):
    CLIENTE = 'cliente'
    PROVEEDOR = 'proveedor'
    
    ROLE_CHOICES = [
        (CLIENTE, 'Cliente'),
        (PROVEEDOR, 'Proveedor'),
    ]

    email = models.EmailField(unique=True)
    
    user_type = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES,
        default=CLIENTE,
        verbose_name="Tipo de Usuario"
    )
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
        return f"{self.username} ({self.get_user_type_display()})"

class ProviderApplication(models.Model):
    nombre_completo = models.CharField(max_length=150)
    nombre_negocio = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    domicilio = models.CharField(max_length=255)
    
    # Documentación
    documento_identidad = models.FileField(upload_to='proveedores/documentos/identidad/')
    certificado_productos = models.FileField(upload_to='proveedores/documentos/certificados/', null=True, blank=True)
    registro_marca = models.FileField(upload_to='proveedores/documentos/marcas/', null=True, blank=True)
    
    # Información de Productos
    listado_productos = models.TextField(blank=True)
    origen_productos = models.TextField(blank=True)
    
    # Control
    aprobada = models.BooleanField(default=False)
    rechazada = models.BooleanField(default=False)
    creada_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Solicitud de {self.nombre_negocio} ({self.email})"

    class Meta:
        verbose_name = "Solicitud de Proveedor"
        verbose_name_plural = "Solicitudes de Proveedores"

class ProviderProfile(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_proveedor')
    nombre_negocio = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    foto_perfil = models.ImageField(upload_to='proveedores/perfiles/', null=True, blank=True)
    
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('en_revision', 'En Revisión'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='en_revision')
    
    email_contacto = models.EmailField(blank=True)
    telefono_contacto = models.CharField(max_length=20, blank=True)
    domicilio_negocio = models.CharField(max_length=255, blank=True)
    
    whatsapp = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    color_fondo = models.CharField(max_length=7, default='#ffffff')

    def __str__(self):
        return f"Perfil de {self.nombre_negocio}"

    class Meta:
        verbose_name = "Perfil de Proveedor"
        verbose_name_plural = "Perfiles de Proveedores"
