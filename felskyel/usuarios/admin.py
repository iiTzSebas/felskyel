from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, ProviderApplication, ProviderProfile
from .forms import RegistroForm
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from django.utils.crypto import get_random_string

# Definimos un Inline para el perfil del proveedor
# Esto permite editar el perfil del negocio dentro de la página del Usuario
class ProviderProfileInline(admin.StackedInline):
    model = ProviderProfile
    can_delete = False
    verbose_name_plural = 'Información del Negocio (Perfil de Proveedor)'
    fk_name = 'user'

# Register your models here.
class UsuarioAdmin(UserAdmin):
    add_form = RegistroForm
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_superuser','is_active' )
    
    # Agregamos el inline aquí para que se vea dentro del usuario
    inlines = (ProviderProfileInline,)

    #campos que se mostraran al editar un usuario 
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Información Personal', {'fields': ('user_type', 'es_mayor_edad')}),
        ('permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'user_type', 'es_mayor_edad', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)
    
admin.site.register(Usuario, UsuarioAdmin)

@admin.register(ProviderApplication)
class ProviderApplicationAdmin(admin.ModelAdmin):
    list_display = ('nombre_negocio', 'email', 'aprobada', 'rechazada', 'creada_en')
    actions = ['aprobar_solicitud', 'rechazar_solicitud']

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-creada_en')

    def save_model(self, request, obj, form, change):
        """
        Se ejecuta cuando haces clic en 'Guardar' dentro del formulario.
        Si marcas 'aprobada' manualmente, disparamos la creación del proveedor.
        """
        if obj.aprobada and not ProviderProfile.objects.filter(user__email=obj.email).exists():
            self._procesar_aprobacion(obj)
        super().save_model(request, obj, form, change)

    def aprobar_solicitud(self, request, queryset):
        """
        Se ejecuta desde el menú desplegable 'Acciones' en la lista.
        """
        for solicitud in queryset:
            self._procesar_aprobacion(solicitud)
        self.message_user(request, "Proveedores creados exitosamente.")

    def _procesar_aprobacion(self, solicitud):
        """
        Lógica robusta para crear/actualizar usuario y perfil.
        """
        with transaction.atomic():
            # 1. Buscar si el usuario ya existe por email
            user = Usuario.objects.filter(email=solicitud.email).first()
            
            if not user:
                # Crear usuario nuevo si no existe
                username = solicitud.email.split('@')[0]
                # Evitar duplicados de username (ej: si dos personas tienen el mismo nombre antes del @)
                if Usuario.objects.filter(username=username).exists():
                    username = f"{username}_{Usuario.objects.count()}"
                
                user = Usuario.objects.create_user(
                    username=username,
                    email=solicitud.email,
                    password=get_random_string(12),
                    user_type=Usuario.PROVEEDOR
                )
            else:
                # Si el usuario ya existía (ej: era cliente), solo cambiamos su rol
                user.user_type = Usuario.PROVEEDOR
                user.save()

            # 2. Crear o actualizar el perfil del proveedor
            ProviderProfile.objects.update_or_create(
                user=user,
                defaults={
                    'nombre_negocio': solicitud.nombre_negocio,
                    'email_contacto': solicitud.email,
                    'telefono_contacto': solicitud.telefono,
                    'domicilio_negocio': solicitud.domicilio,
                    'estado': 'activo'
                }
            )
            
            # Marcar la solicitud como aprobada y asegurar que no esté rechazada
            solicitud.aprobada = True
            solicitud.rechazada = False
            solicitud.save()
            
            # 3. Enviar Correo de bienvenida
            send_mail(
                '¡Bienvenido a la comunidad de proveedores de Felskyel!',
                f'Tu solicitud para "{solicitud.nombre_negocio}" ha sido aprobada. Ya puedes ingresar a tu panel de control.',
                settings.DEFAULT_FROM_EMAIL,
                [solicitud.email],
                fail_silently=True
            )

    def rechazar_solicitud(self, request, queryset):
        for solicitud in queryset:
            if not solicitud.aprobada and not solicitud.rechazada:
                solicitud.rechazada = True
                solicitud.save()
                send_mail(
                    'Actualización de Solicitud',
                    f'Tu solicitud para "{solicitud.nombre_negocio}" ha sido rechazada.',
                    settings.DEFAULT_FROM_EMAIL,
                    [solicitud.email],
                )
        self.message_user(request, "Solicitudes rechazadas.")

@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = ('nombre_negocio', 'user', 'estado', 'email_contacto')
    search_fields = ('nombre_negocio', 'user__email', 'user__username')
