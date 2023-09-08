from django.urls import path
from . import views

app_name = 'permisos'
urlpatterns = [
    path('ver/', views.verPermisos, name='create_rol'),
]
