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
    Funcion que comprueba si el usuario es administrador de categorias (tiene el permiso "Administrar categorias")
    :param user: usuario a comprobar (User)
    :return: True si es administrador de categorias, False en caso contrario
    """
    
    return user.admin_categorias()

@user_passes_test(user_adminCategorias)
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

@user_passes_test(user_adminCategorias)
def verCategorias(request):
    categoria = Categoria.obtener_todos()
    return render(request, 'categorias/verCategorias.html', {'categorias': categoria})

@user_passes_test(user_adminCategorias)
def borrarCategoria(request, categoriaId):

    categoria = Categoria.getById(categoriaId)

    if request.method == 'POST':
        categoria.eliminar()
        return redirect('categorias:ver_categorias')

    return render(request, 'categorias/verCategorias.html', {'categorias': Categoria.obtener_todos()})

@user_passes_test(user_adminCategorias)
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
