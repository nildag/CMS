from django.shortcuts import render

# Create your views here.
from .models import Categoria
from django.shortcuts import render, redirect
from .forms import CategoriaForm
from django.shortcuts import render, redirect, get_object_or_404

def crearCategorias(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categorias:ver_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'categorias/crearCategorias.html', {'form': form})

def verCategorias(request):
    categoria = Categoria.obtener_todos()
    return render(request, 'categorias/verCategorias.html', {'categorias': categoria})

def borrarCategoria(request, categoriaId):

    categoria = Categoria.getById(categoriaId)

    if request.method == 'POST':
        categoria.eliminar()
        return redirect('categorias:ver_categorias')

    return render(request, 'categorias/verCategorias.html', {'categorias': Categoria.obtener_todos()})

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
