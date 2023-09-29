# Create your views here.
from django.shortcuts import render, redirect
from .models import Contenido
from .forms import ContenidoForm

def crearContenido(request):
    if request.method == 'POST':
        form = ContenidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contenido:lista_contenido')
    else:
        form = ContenidoForm()
    return render(request, 'contenido/crearContenido.html', {'form': form})

def listaContenido(request):
    contenido = Contenido.objects.all()
    return render(request, 'contenido/listaContenido.html', {'contenidos': contenido})

def verContenido(request, id):
    contenido = Contenido.objects.get(id=id)
    return render(request, 'contenido/verContenido.html', {'contenido': contenido})