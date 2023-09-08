from django.shortcuts import render

# Create your views here.
from .models import Categoria
from django.shortcuts import render, redirect
from .forms import CategoriaForm
from permisos.models import Permisos

def crear_categorias(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categorias:ver_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'crearCategorias.html', {'form': form})

def verCategorias(request):
    categoria = Categoria.obtener_todos()
    return render(request, 'verCategorias.html', {'categorias': categoria})
