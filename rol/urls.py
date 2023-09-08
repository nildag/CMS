from django.urls import path

from . import views

app_name = 'rol'
urlpatterns = [
    path('crear/', views.crearRol, name='crear_rol'),
    path('ver/', views.verRoles, name='ver_rol'),
]
