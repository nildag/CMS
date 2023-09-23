from django.shortcuts import render

# Create your views here.
from .models import Categoria
from django.shortcuts import render, redirect
from .forms import CategoriaForm
from permiso.models import Permiso

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
