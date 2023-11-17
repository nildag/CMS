from django.shortcuts import render
from usuario.models import User
from usuario.models import UserCategoria

def home(request):
    """
    Vista de la página de inicio.

    Esta vista muestra la página de inicio del sitio web.

    :param request: La solicitud HTTP.
    :return: La página de inicio.
    """

    if request.user.id == 1 and request.user.last_login.strftime("%Y-%m-%d %H:%M:%S") == request.user.date_joined.strftime("%Y-%m-%d %H:%M:%S"):
        user = User.objects.get(id=1)
        user_categoria = UserCategoria.objects.get(id=1)
        user_categoria.rol_id = 6
        user_categoria.save()


    return render(request, 'home/home.html')

def profile(request):
    """
    Vista del perfil de usuario.

    Esta vista muestra la página de perfil del usuario.

    :param request: La solicitud HTTP.
    :return: La página de perfil del usuario.
    """
    return render(request, 'account/profile.html')

def administrar(request):
    """
    Vista para la sección de administración.

    Esta vista muestra la página de administración del sitio web.

    :param request: La solicitud HTTP.
    :return: La página de administración.
    """
    return render(request, 'administrar/administrar.html')
