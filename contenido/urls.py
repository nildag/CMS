from django.urls import path
from . import views

app_name = 'contenido'
urlpatterns = [
    path('crear/', views.crearContenido, name='crear_contenido'),
    path('lista/', views.listaContenido, name='lista_contenido'),
    path('ver/<int:id>/', views.verContenido, name='ver_contenido')
]