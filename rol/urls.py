from django.urls import path

from . import views

app_name = 'rol'
urlpatterns = [
    path('crear/', views.crear_rol, name='crear_rol'),
    path('lista_roles/', views.lista_roles, name='lista_roles'),
    path('borrar_rol/<int:rol_id>/', views.borrar_rol, name='borrar_rol'),
    path('lista_permisos/<int:rol_id>/', views.lista_permisos, name='lista_permisos'),
    path('editar_rol/<int:rol_id>/', views.editar_rol, name='editar_rol'),
]