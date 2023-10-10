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

def user_admin(user):

    """
    Funcion que verifica si el usuario es administrador
    :param user: usuario
    :return: True si el usuario es administrador, False si no lo es (boolean)
    """

    return user.is_superuser

@user_passes_test(user_admin)
def crearCategorias(request):
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

@user_passes_test(user_admin)
def verCategorias(request):
    categoria = Categoria.obtener_todos()
    return render(request, 'categorias/verCategorias.html', {'categorias': categoria})

@user_passes_test(user_admin)
def borrarCategoria(request, categoriaId):

    categoria = Categoria.getById(categoriaId)

    if request.method == 'POST':
        categoria.eliminar()
        return redirect('categorias:ver_categorias')

    return render(request, 'categorias/verCategorias.html', {'categorias': Categoria.obtener_todos()})

@user_passes_test(user_admin)
def editarCategoria(request, categoriaId):

    categoria = Categoria.getById(categoriaId)

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('categorias:ver_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categorias/crearCategorias.html', {'form': form})
