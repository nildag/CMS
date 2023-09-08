from django.urls import path

from . import views

app_name = 'rol'
urlpatterns = [
    path('crear/', views.crear_rol, name='crear_rol'),
    path('ver/', views.verRoles, name='ver_rol'),
]
