from django.shortcuts import render
from permisos.models import Permisos


def verPermisos(request):
    permisos = Permisos().permisos
    return render(request, 'ver_permisos.html', {'permisos': permisos})
