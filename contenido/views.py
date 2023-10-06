from django.contrib.auth.decorators import login_required
from .models import Contenido
from .forms import ContenidoForm
from usuario.models import UserCategoria
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

@login_required
def crearContenido(request):
    """
    Vista para crear nuevo contenido. Requiere autenticación.

    Args:
        request: Objeto de solicitud HTTP.

    Returns:
        HttpResponse: Respuesta HTTP que redirige a la lista de contenidos o muestra el formulario de creación.
    """
    categorias_autor = UserCategoria.objects.filter(user=request.user, rol__nombre='Autor').values_list('categoria__id', flat=True)
    
    if request.method == 'POST':
        form = ContenidoForm(request.POST, autor=request.user)
        if form.is_valid():
            contenido = form.save(commit=False)
            contenido.autor = request.user
            contenido.save()
            return redirect('contenido:lista_contenido')
    else:
        form = ContenidoForm(categorias_autor=categorias_autor, autor=request.user)
    
    return render(request, 'contenido/crearContenido.html', {'form': form})

@login_required
def editarContenido(request, id):
    """
    Vista para editar contenido existente. Requiere autenticación.

    Args:
        request: Objeto de solicitud HTTP.
        id (int): ID del contenido a editar.

    Returns:
        HttpResponse: Respuesta HTTP que redirige a la lista de contenidos o muestra el formulario de edición.
    """
    categorias_autor = UserCategoria.objects.filter(user=request.user, rol__nombre='Autor').values_list('categoria__id', flat=True)
    contenido = get_object_or_404(Contenido, id=id)
    if request.method == 'POST':
        form = ContenidoForm(request.POST, instance=contenido, autor=request.user, categorias_autor=categorias_autor)
        if form.is_valid():
            form.save()
            return redirect('contenido:lista_contenido')
    else:
        form = ContenidoForm(instance=contenido, categorias_autor=categorias_autor, autor=request.user)
    return render(request, 'contenido/editarContenido.html', {'form': form})

@login_required
def eliminarContenido(request, id):
    """
    Vista para eliminar contenido existente. Requiere autenticación.

    Args:
        request: Objeto de solicitud HTTP.
        id (int): ID del contenido a eliminar.

    Returns:
        HttpResponse: Respuesta HTTP que redirige a la lista de contenidos.
    """
    contenido = get_object_or_404(Contenido, id=id)
    contenido.delete()
    return redirect('contenido:lista_contenido')

@login_required
def confirmarEliminarContenido(request, id):
    """
    Vista para confirmar la eliminación de un contenido existente. Requiere autenticación.

    Args:
        request: Objeto de solicitud HTTP.
        id (int): ID del contenido a confirmar la eliminación.

    Returns:
        HttpResponse: Respuesta HTTP que muestra la página de confirmación de eliminación.
    """
    contenido = get_object_or_404(Contenido, id=id)
    return render(request, 'contenido/confirmarEliminarContenido.html', {'contenido': contenido})

def listaContenido(request):
    """
    Vista para mostrar la lista de contenidos.

    Args:
        request: Objeto de solicitud HTTP.

    Returns:
        HttpResponse: Respuesta HTTP que muestra la lista de contenidos.
    """
    contenido = Contenido.objects.all()
    return render(request, 'contenido/listaContenido.html', {'contenidos': contenido})

def verContenido(request, id):
    """
    Vista para ver un contenido específico. No requiere autenticación.

    Args:
        request: Objeto de solicitud HTTP.
        id (int): ID del contenido a visualizar.

    Returns:
        HttpResponse: Respuesta HTTP que muestra la página del contenido específico.
    """
    contenido = Contenido.objects.get(id=id)
    return render(request, 'contenido/verContenido.html', {'contenido': contenido})
