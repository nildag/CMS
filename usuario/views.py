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
    usuarios = User.objects.all()
    return render(request, 'usuario/verUsuarios.html', {'usuarios': usuarios})

@user_passes_test(user_admin_asigRoles)
def listaUserCategoria(request, idUsuario):
    usuario = User.objects.get(id=idUsuario)
    userCategoriasRoles = UserCategoria.objects.filter(user=usuario)
    # Ordenamos por el nombre de la categoria
    userCategoriasRoles = userCategoriasRoles.order_by('categoria__nombre')
    return render(request, 'usuario/listaUserCategoria.html', {'userCategoriasRoles': userCategoriasRoles, 'usuario': usuario})

@user_passes_test(user_admin_asigRoles)
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

@user_passes_test(user_admin_asigRoles)
def eliminarUserCategoria(request, idUserCategoria):
    userCategoria = UserCategoria.objects.get(id=idUserCategoria)
    usuario = userCategoria.user
    userCategoria.delete()
    return redirect('usuario:listaUserCategoria', idUsuario=usuario.id)

@user_passes_test(user_admin_asigRoles)
def editarUserCategoria(request, idUserCategoria):
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

    # El usuario recién se registra
    if request.user.registrado == True:

        # Al usuario se le asigna el rol Suscriptor por defecto en todas las categorias
        categorias = Categoria.objects.all()
        for categoria in categorias:

            rol = Rol.objects.get(nombre='Suscriptor')
            userCategoria = UserCategoria()

            userCategoria.user = request.user
            userCategoria.categoria = categoria
            userCategoria.rol = rol
            userCategoria.save()

        # Se cambia el estado del usuario a registrado
        request.user.registrado = False
        request.user.save()
        
    # Redirecciona a la pagina principal
    return redirect('home')