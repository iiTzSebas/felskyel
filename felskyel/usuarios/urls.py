from django.urls import path
from . import views

urlpatterns = [
    path('reggistro', views.reggistro_view, name='reggsitro'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('p/', views.p_view, name='p'),
]