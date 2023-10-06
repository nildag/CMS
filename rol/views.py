from .models import Rol
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RolForm
from permiso.models import Permiso


def crear_rol(request):
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rol:lista_roles')
    else:
        form = RolForm()
    return render(request, 'rol/crearRol.html', {'form': form})

def lista_roles(request):
    roles = Rol.getAll()
    return render(request, 'rol/lista_roles.html', {'roles': roles})

def borrar_rol(request, rol_id):
    rol = get_object_or_404(Rol, pk=rol_id)

    if request.method == 'POST':
        rol.delete()
        return redirect('rol:lista_roles')

    return render(request, 'rol/lista_roles.html', {'roles': Rol.objects.all()})

def lista_permisos(request, rol_id):
    rol = get_object_or_404(Rol, pk=rol_id)
    return render(request, 'rol/lista_permisos.html', {'rol': rol})

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