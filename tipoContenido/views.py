from django.shortcuts import render

# Create your views here.
from .models import tipoContenido
from django.shortcuts import render, redirect
from .forms import tipoContenidoForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required


def user_admin_tipoContenido(user):
    """
    Función que comprueba si el usuario es administrador de tipo de contenido (tiene el permiso "Administrar tipo de contenido").

    :param user: El usuario a comprobar (User).
    :return: True si es administrador de tipo de contenido, False en caso contrario.
    """
    return user.admin_tipo_contenido


@login_required
@user_passes_test(user_admin_tipoContenido)
def crearTipoContenido(request):
    """
    Vista para crear un nuevo tipo de contenido.

    :param request: La solicitud HTTP.
    :return: La página de creación de tipo de contenido o redirecciona a la lista de tipo de contenido si se crea con éxito.
    """
    if request.method == 'POST':
        form = tipoContenidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tipoContenido:ver_tipo_de_contenido')
    else:
        form = tipoContenidoForm()

    return render(request, 'tipoContenido/crear_tipo_de_contenido.html', {'form': form})


@login_required
@user_passes_test(user_admin_tipoContenido)
def verTipoContenido(request):
    """
    Vista para mostrar la lista de tipos de contenido.

    :param request: La solicitud HTTP.
    :return: La página de lista de tipos de contenido.
    """
    tipoDContenido = tipoContenido.obtener_todos()
    return render(request, 'tipoContenido/ver_tipo_de_contenido.html', {'tipoContenido': tipoDContenido})


@login_required
@user_passes_test(user_admin_tipoContenido)
def borrarTipoContenido(request, tipoContenidoId):
    """
    Vista para eliminar un tipo de contenido.

    :param request: La solicitud HTTP.
    :param tipoContenidoId: El ID del tipo de contenido a eliminar.
    :return: La página de lista de tipos de contenido o redirecciona a la lista de tipos de contenido si se elimina con éxito.
    """
    tipoDContenido = tipoContenido.getById(tipoContenidoId)

    if request.method == 'POST':
        tipoDContenido.eliminar()
        return redirect('tipoContenido:ver_tipo_de_contenido')

    return render(request, 'tipoContenido/ver_tipo_de_contenido.html',
                  {'tipoContenido': tipoDContenido.obtener_todos()})


@login_required
@user_passes_test(user_admin_tipoContenido)
def editarTipoContenido(request, tipoContenidoId):
    """
    Vista para editar un tipo de contenido existente.

    :param request: La solicitud HTTP.
    :param tipoContenidoId: El ID del tipo de contenido a editar.
    :return: La página de edición de tipos de contenido o redirecciona a la lista de tipos de contenido si se edita con éxito.
    """
    tipoDContenido = tipoContenido.getById(tipoContenidoId)

    if request.method == 'POST':
        form = tipoContenidoForm(request.POST, instance=tipoDContenido)
        if form.is_valid():
            form.save()
            return redirect('tipoContenido:ver_tipo_de_contenido')
    else:
        form = tipoContenidoForm(instance=tipoDContenido)
    return render(request, 'tipoContenido/crear_tipo_de_contenido.html', {'form': form})

