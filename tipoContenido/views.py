from django.shortcuts import render

# Create your views here.
from .models import tipoContenido
from django.shortcuts import render, redirect
from .forms import tipoContenidoForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

def user_admin_tipoContenido(user):

    """
    Funcion que comprueba si el usuario es administrador de tipo de contenido (tiene el permiso "Administrar tipo de contenido")
    :param user: usuario a comprobar (User)
    :return: True si es administrador de tipo de contenido, False en caso contrario
    """

    return user.admin_tipo_contenido

@login_required
@user_passes_test(user_admin_tipoContenido)
def crearTipoContenido(request):
    if request.method == 'POST':
        form = tipoContenidoForm(request.POST)
        if form.is_valid():
            form.save()
            # Si el formulario es válido, puedes redirigir al usuario a la página deseada.
            return redirect('tipoContenido:ver_tipo_de_contenido')
        # Si el formulario no es válido, puedes mostrar el formulario con errores.
    else:
        form = tipoContenidoForm()

    return render(request, 'tipoContenido/crear_tipo_de_contenido.html', {'form': form})

@login_required
@user_passes_test(user_admin_tipoContenido)
def verTipoContenido(request):
    tipoDContenido = tipoContenido.obtener_todos()
    return render(request, 'tipoContenido/ver_tipo_de_contenido.html', {'tipoContenido': tipoDContenido})

@login_required
@user_passes_test(user_admin_tipoContenido)
def borrarTipoContenido(request, tipoContenidoId):

    tipoDContenido = tipoContenido.getById(tipoContenidoId)

    if request.method == 'POST':
        tipoDContenido.eliminar()
        return redirect('tipoContenido:ver_tipo_de_contenido')

    return render(request, 'tipoContenido/ver_tipo_de_contenido.html', {'tipoContenido': tipoDContenido.obtener_todos()})

@login_required
@user_passes_test(user_admin_tipoContenido)
def editarTipoContenido(request, tipoContenidoId):

    tipoDContenido = tipoContenido.getById(tipoContenidoId)

    if request.method == 'POST':
        form = tipoContenidoForm(request.POST, instance=tipoDContenido)
        if form.is_valid():
            form.save()
            return redirect('tipoContenido:ver_tipo_de_contenido')
    else:
        form = tipoContenidoForm(instance=tipoDContenido)
    return render(request, 'tipoContenido/crear_tipo_de_contenido.html', {'form': form})

