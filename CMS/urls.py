from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("rol/", include('rol.urls')),
    path("permiso/", include('permiso.urls')),
    path("", include('home.urls')),
    path("accounts/", include('allauth.urls')),
    path("categorias/", include('categorias.urls')),
    path("usuario/", include('usuario.urls')),
    path("contenido/", include('contenido.urls')),
]
