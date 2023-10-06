from django.urls import path

from . import views

app_name = 'categorias'
urlpatterns = [
    path('crear/', views.crearCategorias, name='crear_categorias'),
    path('ver/', views.verCategorias, name='ver_categorias'),
    path('borrar/<int:categoriaId>/', views.borrarCategoria, name='borrar_categoria'),
    path('editar/<int:categoriaId>/', views.editarCategoria, name='editar_categoria'),
]
