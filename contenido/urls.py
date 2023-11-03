from django.urls import path
from . import views

app_name = 'contenido'
urlpatterns = [
    path('crear/', views.crearContenido, name='crear_contenido'),
    path('lista/', views.listaContenido, name='lista_contenido'),
    path('ver/<int:id>/', views.verContenido, name='ver_contenido'),
    path('editar/<int:id>/', views.editarContenido, name='editar_contenido'),
    path('eliminar/<int:id>/', views.eliminarContenido, name='eliminar_contenido'),
    path('eliminar/<int:id>/confirmar/', views.confirmarEliminarContenido, name='confirmar_eliminar_contenido'),
    path('listaTodos/', views.listaTodos, name='lista_todos'),
    path('listaPublicador/', views.listaPublicador, name='lista_publicador'),
    path('listaEditor/', views.listaEditor, name='lista_editor'),
    path('valorar/<int:id>/', views.valorarContenido, name='valorar_contenido'),
    path('buscar/', views.buscarContenido, name='buscar_contenido'),
    path('aEdicion/<int:id>/', views.aEdicion, name='a_edicion'),
    path('aPublicacion/<int:id>/', views.aPublicacion, name='a_publicacion'),
    path('publicar/<int:id>/', views.publicarContenido, name='publicar_contenido'),
    path('kanban/', views.kanbanView, name='kanban'),
]
