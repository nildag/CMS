from django.contrib.auth.decorators import login_required
from .models import Contenido
from .models import Categoria
from .forms import ContenidoForm
from usuario.models import UserCategoria
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from usuario.models import User
from contenido.models import Valoracion
from django.db.models import Q

def user_autor(user):

    """
    Funcion que comprueba si el usuario es autor (tiene el permiso "Crear contenido")
    :param user: usuario a comprobar (User)
    :return: True si es autor, False en caso contrario
    """

    return User.user_is_autor(user)

def user_editor(user):

    """
    Funcion que comprueba si el usuario es editor (tiene el permiso "Editar contenido")
    :param user: usuario a comprobar (User)
    :return: True si es editor, False en caso contrario
    """

    return User.is_editor(user)

def user_publicador(user):

    """
    Funcion que comprueba si el usuario es publicador (tiene el permiso "Publicar contenido")
    :param user: usuario a comprobar (User)
    :return: True si es publicador, False en caso contrario
    """

    return User.is_publicador(user)

def user_autor_or_editor(user):

    """
    Funcion que comprueba si el usuario es autor o editor
    :param user: usuario a comprobar (User)
    :return: True si es autor o editor, False en caso contrario
    """

    return user_autor(user) or user_editor(user)

@login_required
@user_passes_test(user_autor)
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
@user_passes_test(user_autor_or_editor)
def editarContenido(request, id):
    """
    Vista para editar contenido existente. Requiere autenticación.

    Args:
        request: Objeto de solicitud HTTP.
        id (int): ID del contenido a editar.

    Returns:
        HttpResponse: Respuesta HTTP que redirige a la lista de contenidos o muestra el formulario de edición.
    """
    if user_autor(request.user):
        categorias_autor = UserCategoria.objects.filter(user=request.user, rol__nombre='Autor').values_list('categoria__id', flat=True)
    else:
        categorias_autor = Contenido.objects.filter(id=id).values_list('categoria__id', flat=True)

    contenido = get_object_or_404(Contenido, id=id)
    if request.method == 'POST':
        form = ContenidoForm(request.POST, instance=contenido, autor=request.user, categorias_autor=categorias_autor)
        if form.is_valid():
            form.save()
            
            if user_autor(request.user):
                return redirect('contenido:lista_contenido')
            else:
                return redirect('contenido:lista_editor')
        
    else:
        form = ContenidoForm(instance=contenido, categorias_autor=categorias_autor, autor=request.user)
    return render(request, 'contenido/editarContenido.html', {'form': form})

@login_required
@user_passes_test(user_autor)
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

@login_required
@user_passes_test(user_autor)
def listaContenido(request):

    """
    Vista para listar los contenidos de un usuario
    :param request: Objeto de solicitud HTTP.
    :return: HttpResponse: Respuesta HTTP que muestra la lista de contenidos.
    """

    user = User.objects.get(id=request.user.id)
    contenido = Contenido.for_user(user)
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

def listaTodos(request):
    """
    Vista para mostrar la lista de contenidos de todos los usuarios.
    :param request: Objeto de solicitud HTTP.
    :return: HttpResponse: Respuesta HTTP que muestra la lista de contenidos.
    """
    contenido = Contenido.objects.all()
    categorias = Categoria.objects.all()  # Obtener todas las categorías
    return render(request, 'contenido/listaTodos.html', {'contenidos': contenido, 'categorias': categorias})


@login_required
@user_passes_test(user_publicador)
def listaPublicador(request):

    """
    Vista para mostrar la lista de contenidos de los usuarios publicadores.
    :param request: Objeto de solicitud HTTP.
    :return: HttpResponse: Respuesta HTTP que muestra la lista de contenidos.
    """

    user = User.objects.get(id=request.user.id)
    categorias = UserCategoria.objects.filter(user=user, rol__nombre='Publicador').values_list('categoria__id', flat=True)
    contenido = Contenido.for_categorias(categorias)
    return render(request, 'contenido/listaPublicador.html', {'contenidos': contenido})

@login_required
@user_passes_test(user_editor)
def listaEditor(request):

    """
    Vista para mostrar la lista de contenidos de los usuarios editores.
    :param request: Objeto de solicitud HTTP.
    :return: HttpResponse: Respuesta HTTP que muestra la lista de contenidos.
    """

    user = User.objects.get(id=request.user.id)
    categorias = UserCategoria.objects.filter(user=user, rol__nombre='Editor').values_list('categoria__id', flat=True)
    contenido = Contenido.for_categorias(categorias)
    return render(request, 'contenido/listaEditor.html', {'contenidos': contenido})

@login_required
def valorarContenido(request, id):
    """
    Vista para valorar un contenido específico. Requiere autenticación.

    Args:
        request: Objeto de solicitud HTTP.
        id (int): ID del contenido a valorar.

    Returns:
        HttpResponse: Redirige a la página del contenido valorado o muestra un mensaje de error.
    """
    if request.method == 'POST':
        contenido = get_object_or_404(Contenido, id=id)
        puntuacion = int(request.POST.get('puntuacion'))  # Asume que tienes un formulario con un campo 'puntuacion'

        # Comprueba si el usuario ya ha valorado este contenido
        valoracion_existente = Valoracion.objects.filter(contenido=contenido, usuario=request.user).first()
        if valoracion_existente:
            # Actualiza la valoración si el usuario ya ha valorado este contenido
            valoracion_existente.puntuacion = puntuacion
            valoracion_existente.save()
        else:
            # Crea una nueva valoración si el usuario no ha valorado este contenido
            valoracion = Valoracion(contenido=contenido, usuario=request.user, puntuacion=puntuacion)
            valoracion.save()

        # Recalcula la puntuación promedio del contenido y el número de valoraciones
        valoraciones = Valoracion.objects.filter(contenido=contenido)
        total_puntuacion = sum(valoracion.puntuacion for valoracion in valoraciones)
        numero_valoraciones = valoraciones.count()
        contenido.puntuacion = total_puntuacion / numero_valoraciones
        contenido.numero_valoraciones = numero_valoraciones
        contenido.save()

        return redirect('contenido:ver_contenido', id=id)
    else:
        # Muestra el contenido específico para que el usuario pueda valorarlo
        contenido = get_object_or_404(Contenido, id=id)
        return render(request, 'contenido/valorarContenido.html', {'contenido': contenido})


def buscarContenido(request):
    """
    Vista para buscar contenidos por título de contenido o nombre de categoría.

    Args:
        request: Objeto de solicitud HTTP.

    Returns:
        HttpResponse: Respuesta HTTP que muestra los resultados de la búsqueda.
    """
    query = request.GET.get('q')

    contenidos = Contenido.objects.filter(
        Q(titulo__icontains=query) |
        Q(categoria__nombre__icontains=query) |
        Q(autor__first_name__icontains=query) |
        Q(autor__last_name__icontains=query)
    )

    return render(request, 'contenido/listaTodos.html', {'contenidos': contenidos, 'categorias': Categoria.objects.all()})