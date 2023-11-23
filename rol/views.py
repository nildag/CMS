from .models import Rol
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RolForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

def tiene_permiso_administrar_roles(user):
    """
    Función que comprueba si el usuario tiene el permiso "Administrar roles".
    :param user: El usuario a comprobar (User).
    :return: True si tiene el permiso, False en caso contrario.
    """
    return user.tiene_permiso_administrar_roles()

@login_required
@user_passes_test(tiene_permiso_administrar_roles)
def crear_rol(request):
    """
    Vista para crear un nuevo rol.
    :param request: La solicitud HTTP.
    :return: La página de creación de roles o redirecciona a la lista de roles si se crea con éxito.
    """
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rol:lista_roles')
    else:
        form = RolForm()
    return render(request, 'rol/crearRol.html', {'form': form})

@login_required
@user_passes_test(tiene_permiso_administrar_roles)
def lista_roles(request):
    """
    Vista para mostrar la lista de roles.
    :param request: La solicitud HTTP.
    :return: La página de lista de roles.
    """
    roles = Rol.getAll()
    roles = roles.order_by('-last_modification', 'nombre')
    return render(request, 'rol/lista_roles.html', {'roles': roles})

@login_required
@user_passes_test(tiene_permiso_administrar_roles)
def borrar_rol(request, rol_id):
    """
    Vista para eliminar un rol.
    :param request: La solicitud HTTP.
    :param rol_id: El ID del rol a eliminar.
    :return: La página de lista de roles o redirecciona a la lista de roles si se elimina con éxito.
    """
    rol = get_object_or_404(Rol, pk=rol_id)

    if request.method == 'POST':
        rol.delete()
        return redirect('rol:lista_roles')

    return render(request, 'rol/lista_roles.html', {'roles': Rol.objects.all()})

@login_required
@user_passes_test(tiene_permiso_administrar_roles)
def lista_permisos(request, rol_id):
    """
    Vista para mostrar los permisos de un rol.

    :param request: La solicitud HTTP.
    :param rol_id: El ID del rol cuyos permisos se mostrarán.
    :return: La página de lista de permisos de un rol.
    """
    rol = get_object_or_404(Rol, pk=rol_id)
    return render(request, 'rol/lista_permisos.html', {'rol': rol})

@login_required
@user_passes_test(tiene_permiso_administrar_roles)
def editar_rol(request, rol_id):
    """
    Vista para editar un rol existente.
    :param request: La solicitud HTTP.
    :param rol_id: El ID del rol a editar.
    :return: La página de edición de roles o redirecciona a la lista de roles si se edita con éxito.
    """
    rol = get_object_or_404(Rol, pk=rol_id)
    if request.method == 'POST':
        form = RolForm(request.POST, instance=rol)
        if form. is_valid():
            form.save()
            return redirect('rol:lista_roles')
    else:
        form = RolForm(instance=rol)
    return render(request, 'rol/crearRol.html', {'form': form})
