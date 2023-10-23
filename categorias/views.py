from django.shortcuts import render

# Create your views here.
from .models import Categoria
from django.shortcuts import render, redirect
from .forms import CategoriaForm
from django.shortcuts import render, redirect, get_object_or_404
from rol.models import Rol
from usuario.models import User
from usuario.models import UserCategoria
from django.contrib.auth.decorators import user_passes_test


def user_adminCategorias(user):
    """
    Función que comprueba si el usuario es administrador de categorías (tiene el permiso "Administrar categorías").

    Args:
        user (User): El usuario a comprobar.

    Returns:
        bool: True si es administrador de categorías, False en caso contrario.
    """
    return user.admin_categorias()


@user_passes_test(user_adminCategorias)
def crearCategorias(request):
    """
    Vista para crear una nueva categoría.

    Args:
        request: La solicitud HTTP.

    Returns:
        HttpResponseRedirect: Redirige a la vista de ver categorías.
    """
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            categoria = Categoria.obtener_por_nombre(form.cleaned_data['nombre'])
            rol = Rol.getByNombre('Suscriptor')
            usuarios = User.getAll()

            for usuario in usuarios:
                userCategoria = UserCategoria()
                userCategoria.user = usuario
                userCategoria.rol = rol
                userCategoria.categoria = categoria
                userCategoria.save()

            return redirect('categorias:ver_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'categorias/crearCategorias.html', {'form': form})


@user_passes_test(user_adminCategorias)
def verCategorias(request):
    """
    Vista para ver todas las categorías.

    Args:
        request: La solicitud HTTP.

    Returns:
        render: Renderiza la vista de ver categorías.
    """
    categoria = Categoria.obtener_todos()
    return render(request, 'categorias/verCategorias.html', {'categorias': categoria})


@user_passes_test(user_adminCategorias)
def borrarCategoria(request, categoriaId):
    """
    Vista para borrar una categoría.

    Args:
        request: La solicitud HTTP.
        categoriaId (int): El ID de la categoría a borrar.

    Returns:
        HttpResponseRedirect: Redirige a la vista de ver categorías.
        render: Renderiza la vista de ver categorías.
    """
    categoria = Categoria.getById(categoriaId)

    if request.method == 'POST':
        categoria.eliminar()
        return redirect('categorias:ver_categorias')

    return render(request, 'categorias/verCategorias.html', {'categorias': Categoria.obtener_todos()})


@user_passes_test(user_adminCategorias)
def editarCategoria(request, categoriaId):
    """
    Vista para editar una categoría.

    Args:
        request: La solicitud HTTP.
        categoriaId (int): El ID de la categoría a editar.

    Returns:
        HttpResponseRedirect: Redirige a la vista de ver categorías.
        render: Renderiza la vista de crear categorías.
    """
    categoria = Categoria.getById(categoriaId)

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('categorias:ver_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categorias/crearCategorias.html', {'form': form})
