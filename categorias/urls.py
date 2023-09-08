from django.urls import path

from . import views

app_name = 'categorias'
urlpatterns = [
    path('crear/', views.crearCategorias, name='crear_categorias'),
    path('ver/', views.verCategorias, name='ver_categorias'),
]
