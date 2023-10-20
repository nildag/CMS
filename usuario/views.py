# Create your views here.
from .models import User
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserCategoriaForm
from .models import UserCategoria
from .models import User
from categorias.models import Categoria
from rol.models import Rol
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

def user_admin_asigRoles(user):

    """
    Funcion que comprueba si el usuario es administrador de asignacion de roles (tiene el permiso "Asignar roles")
    :param user: usuario a comprobar (User)
    :return: True si es administrador de asignacion de roles, False en caso contrario
    """

    return user.admin_asigRoles()

@user_passes_test(user_admin_asigRoles)
def verUsuarios(request):
    """
    Vista para mostrar una lista de usuarios.

    :param request: La solicitud HTTP.
    :return: La página de lista de usuarios.
    """
    usuarios = User.objects.all()
    return render(request, 'usuario/verUsuarios.html', {'usuarios': usuarios})

@user_passes_test(user_admin_asigRoles)
def listaUserCategoria(request, idUsuario):
    """
    Vista para mostrar una lista de categorías y roles asignados a un usuario específico.

    :param request: La solicitud HTTP.
    :param idUsuario: El ID del usuario.
    :return: La página de lista de categorías y roles para el usuario especificado.
    """
    usuario = User.objects.get(id=idUsuario)
    userCategoriasRoles = UserCategoria.objects.filter(user=usuario)
    # Ordenamos por el nombre de la categoría
    userCategoriasRoles = userCategoriasRoles.order_by('categoria__nombre')
    return render(request, 'usuario/listaUserCategoria.html', {'userCategoriasRoles': userCategoriasRoles, 'usuario': usuario})

@user_passes_test(user_admin_asigRoles)
def crearUserCategoria(request, idUsuario):
    """
    Vista para crear una asignación de categoría y rol para un usuario específico.

    :param request: La solicitud HTTP.
    :param idUsuario: El ID del usuario.
    :return: La página de creación de asignación de categoría y rol o redirecciona a la lista de asignaciones si se crea con éxito.
    """
    usuario = User.objects.get(id=idUsuario)
    if request.method == 'POST':
        form = UserCategoriaForm(request.POST)
        if form.is_valid():
            form.instance.user = usuario
            userCategoria = form.save(commit=False)
            userCategoria.user = usuario
            userCategoria.save()
            return redirect('usuario:listaUserCategoria', idUsuario=usuario.id)
    else:
        form = UserCategoriaForm(initial={'user': usuario})
    return render(request, 'usuario/crearUserCategoria.html', {'form': form, 'usuario': usuario})

@user_passes_test(user_admin_asigRoles)
def eliminarUserCategoria(request, idUserCategoria):
    """
    Vista para eliminar una asignación de categoría y rol para un usuario.

    :param request: La solicitud HTTP.
    :param idUserCategoria: El ID de la asignación de categoría y rol a eliminar.
    :return: Redirecciona a la lista de asignaciones después de la eliminación.
    """
    userCategoria = UserCategoria.objects.get(id=idUserCategoria)
    usuario = userCategoria.user
    userCategoria.delete()
    return redirect('usuario:listaUserCategoria', idUsuario=usuario.id)

@user_passes_test(user_admin_asigRoles)
def editarUserCategoria(request, idUserCategoria):
    """
    Vista para editar una asignación de categoría y rol para un usuario.

    :param request: La solicitud HTTP.
    :param idUserCategoria: El ID de la asignación de categoría y rol a editar.
    :return: La página de edición de asignación de categoría y rol o redirecciona a la lista de asignaciones si se edita con éxito.
    """
    userCategoria = get_object_or_404(UserCategoria, id=idUserCategoria)
    if request.method == 'POST':
        form = UserCategoriaForm(request.POST, instance=userCategoria)
        if form.is_valid():
            form.save()
            return redirect('usuario:listaUserCategoria', idUsuario=userCategoria.user.id)
    else:
        form = UserCategoriaForm(instance=userCategoria)
    return render(request, 'usuario/crearUserCategoria.html', {'form': form, 'userCategoria': userCategoria})

def index(request):
    """
    Vista para la página de inicio.

    Esta vista verifica si un usuario recién registrado y asigna el rol "Suscriptor" en todas las categorías.

    :param request: La solicitud HTTP.
    :return: Redirecciona a la página principal (home).
    """
    if request.user.registrado:
        categorías = Categoria.objects.all()
        for categoría in categorías:
            rol = Rol.objects.get(nombre='Suscriptor')
            userCategoria = UserCategoria()
            userCategoria.user = request.user
            userCategoria.categoría = categoría
            userCategoria.rol = rol
            userCategoria.save()
        request.user.registrado = False
        request.user.save()
    return redirect('home')
