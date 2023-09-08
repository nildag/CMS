from .models import Rol
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RolForm
from permisos.models import Permisos


def crear_rol(request):
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            form.instance.permisos = Permisos().permisos
            form.save()
            return redirect('rol:lista_roles')
    else:
        form = RolForm()
    return render(request, 'crearRol.html', {'form': form})

def lista_roles(request):
    roles = Rol.objects.all()
    return render(request, 'lista_roles.html', {'roles': roles})

def borrar_rol(request, rol_id):
    rol = get_object_or_404(Rol, pk=rol_id)

    if request.method == 'POST':
        rol.delete()
        return redirect('rol:lista_roles')

    return render(request, 'lista_roles.html', {'roles': Rol.objects.all()})

def modificar_permisos(request, rol_id):
    rol = get_object_or_404(Rol, pk=rol_id)

    if request.method == 'POST':
        pass

    return render(request, 'lista_permisos.html', {'rol': rol})

def guardar_permisos(request, rol_id):
    rol = get_object_or_404(Rol, pk=rol_id)

    if request.method == 'POST':
        for clave, _ in rol.permisos.items():
            nuevo_valor = request.POST.get(clave)
            if nuevo_valor in ['True', 'False']:
                rol.permisos[clave] = nuevo_valor
        rol.save()

    return redirect('rol:lista_permisos', rol_id=rol_id)

