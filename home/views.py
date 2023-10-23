from django.shortcuts import render

def home(request):
    """
    Vista de la página de inicio.

    Esta vista muestra la página de inicio del sitio web.

    :param request: La solicitud HTTP.
    :return: La página de inicio.
    """
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
