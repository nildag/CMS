from django.urls import path
from . import views

app_name = 'usuario'

urlpatterns = [
    path('', views.index, name='usuario'),
    path('verUsuarios/', views.verUsuarios, name='verUsuarios'),
    path('editarUserCategoria/<int:idUserCategoria>/', views.editarUserCategoria, name='editarUserCategoria'),
    path('listaUserCategoria/<int:idUsuario>/', views.listaUserCategoria, name='listaUserCategoria'),
    path('crearUserCategoria/<int:idUsuario>/', views.crearUserCategoria, name='crearUserCategoria'),
    path('eliminarUserCategoria/<int:idUserCategoria>/', views.eliminarUserCategoria, name='eliminarUserCategoria'),
]
