from django.urls import path
from . import views

urlpatterns = [
    path('reggistro', views.reggistro_view, name='reggistro'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('p/', views.p_view, name='p'),
    path('solicitud-proveedor', views.solicitud_proveedor_view, name='solicitud_proveedor'),
    path('mi-perfil', views.mi_perfil_view, name='mi_perfil'),
]