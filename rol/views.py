from .models import Rol
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RolForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

def user_admin_roles(user):

    """
    Funcion que comprueba si el usuario es administrador de roles (tiene el permiso "Administrar roles")
    :param user: usuario a comprobar (User)
    :return: True si es administrador de roles, False en caso contrario
    """

    return user.admin_roles

@login_required
@user_passes_test(user_admin_roles)
def crear_rol(request):
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rol:lista_roles')
    else:
        form = RolForm()
    return render(request, 'rol/crearRol.html', {'form': form})

@login_required
@user_passes_test(user_admin_roles)
def lista_roles(request):
    roles = Rol.getAll()
    roles = roles.order_by('-last_modification', 'nombre')
    return render(request, 'rol/lista_roles.html', {'roles': roles})

@login_required
@user_passes_test(user_admin_roles)
def borrar_rol(request, rol_id):
    rol = get_object_or_404(Rol, pk=rol_id)

    if request.method == 'POST':
        rol.delete()
        return redirect('rol:lista_roles')

    return render(request, 'rol/lista_roles.html', {'roles': Rol.objects.all()})

@login_required
@user_passes_test(user_admin_roles)
def lista_permisos(request, rol_id):
    rol = get_object_or_404(Rol, pk=rol_id)
    return render(request, 'rol/lista_permisos.html', {'rol': rol})

@login_required
@user_passes_test(user_admin_roles)
def editar_rol(request, rol_id):
    rol = get_object_or_404(Rol, pk=rol_id)
    if request.method == 'POST':
        form = RolForm(request.POST, instance=rol)
        if form.is_valid():
            form.save()
            return redirect('rol:lista_roles')
    else:
        form = RolForm(instance=rol)
    return render(request, 'rol/crearRol.html', {'form': form})