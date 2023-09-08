from django.urls import path

from . import views

app_name = 'rol'
urlpatterns = [
    path('crear/', views.crear_rol, name='crear_rol'),
    path('lista_roles/', views.lista_roles, name='lista_roles'),
    path('borrar_rol/<int:rol_id>/', views.borrar_rol, name='borrar_rol'),
    path('modificar_permisos/<int:rol_id>/', views.modificar_permisos, name='modificar_permisos'),
    path('guardar_permisos/<int:rol_id>/', views.guardar_permisos, name='guardar_permisos'),
]