from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

# Register your models here.
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser','is_active' )
    
    #campos que se mostraran al editar un usuario 
    fieldsets = (None, {'fields': ('username', 'email', 'password')}),
    ('permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)
    
admin.site.register(Usuario, UsuarioAdmin)

