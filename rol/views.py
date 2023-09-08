from .models import Rol
from django.shortcuts import render, redirect
from .forms import RolForm
from permisos.models import Permisos

def crear_rol(request):
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            form.instance.permisos = Permisos().permisos
            form.save()
            return redirect('rol:ver_rol')
    else:
        form = RolForm()
    return render(request, 'crear.html', {'form': form})

def verRoles(request):
    roles = Rol.obtener_todos()
    return render(request, 'ver.html', {'roles': roles})