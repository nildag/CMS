# Create your views here.
from .models import User
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserCategoriaForm
from .models import UserCategoria
from .models import User

def verUsuarios(request):
    usuarios = User.objects.all()
    return render(request, 'usuario/verUsuarios.html', {'usuarios': usuarios})

def listaUserCategoria(request, idUsuario):
    usuario = User.objects.get(id=idUsuario)
    userCategoriasRoles = UserCategoria.objects.filter(user=usuario)
    return render(request, 'usuario/listaUserCategoria.html', {'userCategoriasRoles': userCategoriasRoles, 'usuario': usuario})

def crearUserCategoria(request, idUsuario):
    usuario = User.objects.get(id=idUsuario)
    if request.method == 'POST':
        form = UserCategoriaForm(request.POST)
        if form.is_valid():
            form.instance.user = usuario
            userCategoria = form.save(commit=False)
            userCategoria.User = usuario
            userCategoria.save()
            return redirect('usuario:listaUserCategoria', idUsuario=usuario.id)
    else:
        form = UserCategoriaForm(initial={'user': usuario})
    return render(request, 'usuario/crearUserCategoria.html', {'form': form, 'usuario': usuario})

def eliminarUserCategoria(request, idUserCategoria):
    userCategoria = UserCategoria.objects.get(id=idUserCategoria)
    usuario = userCategoria.user
    userCategoria.delete()
    return redirect('usuario:listaUserCategoria', idUsuario=usuario.id)

def editarUserCategoria(request, idUserCategoria):
    userCategoria = get_object_or_404(UserCategoria, id=idUserCategoria)
    if request.method == 'POST':
        form = UserCategoriaForm(request.POST, instance=userCategoria)
        if form.is_valid():
            form.save()
            return redirect('usuario:listaUserCategoria', idUsuario=userCategoria.user.id)
    else:
        form = UserCategoriaForm(instance=userCategoria)
    return render(request, 'usuario/crearUserCategoria.html', {'form': form})