from django.contrib.auth.decorators import login_required
from .models import Contenido
from .forms import ContenidoForm
from usuario.models import UserCategoria
from django.shortcuts import render, redirect

@login_required
def crearContenido(request):
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


def listaContenido(request):
    contenido = Contenido.objects.all()
    return render(request, 'contenido/listaContenido.html', {'contenidos': contenido})

def verContenido(request, id):
    contenido = Contenido.objects.get(id=id)
    return render(request, 'contenido/verContenido.html', {'contenido': contenido})