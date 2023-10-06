from django.urls import path

from . import views

app_name = 'tipoContenido'
urlpatterns = [
    path('crear/', views.crearTipoContenido, name='crear_tipo_de_contenido'),
    path('ver/', views.verTipoContenido, name='ver_tipo_de_contenido'),
    path('borrar/<int:tipoContenidoId>/', views.borrarTipoContenido, name='borrar_tipo_de_contenido'),
    path('editar/<int:tipoContenidoId>/', views.editarTipoContenido, name='editar_tipo_de_contenido'),
]
