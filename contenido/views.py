from django.contrib.auth.decorators import login_required
from .models import Contenido
from .models import Categoria
from .models import tipoContenido
from .forms import ContenidoForm
from .forms import EditorContenidoForm
from usuario.models import UserCategoria
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from usuario.models import User
from contenido.models import Valoracion
from django.db.models import Q
from notify.signals import notificar
from django.utils import timezone
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from collections import defaultdict

def tiene_permiso_visualizar_kanban(user):
    """
    Funcion que comprueba si el usuario tiene el permiso "Visualizar Kanban" en la categoría System, atendiendo que dicho permiso solo tiene sentido en la categoría System.
    :param user: usuario a comprobar (User)
    :return: True tiene el permiso, False en caso contrario (Boolean)
    """
    return user.tiene_permiso_visualizar_kanban()

def tiene_permiso_crear_contenido(user):
    """
    Funcion que comprueba si el usuario tiene el permiso "Crear contenido" en alguna categoria
    :param user: usuario a comprobar (User)
    :return: True tiene el permiso, False en caso contrario (Boolean)
    """
    return user.tiene_permiso_crear_contenido()

def tiene_permiso_eliminar_contenido(user):
    """
    Funcion que comprueba si el usuario tiene el permiso "Eliminar contenido" en alguna categoria
    :param user: usuario a comprobar (User)
    :return: True tiene el permiso, False en caso contrario (Boolean)
    """
    return user.tiene_permiso_eliminar_contenido()

def tiene_permiso_editar_contenido(user):
    """
    Funcion que comprueba si el usuario tiene el permiso "Editar contenido" en alguna categoria
    :param user: usuario a comprobar (User)
    :return: True tiene el permiso, False en caso contrario (Boolean)
    """
    return user.tiene_permiso_editar_contenido()

def tiene_permiso_publicar_contenido(user):
    """
    Funcion que comprueba si el usuario tiene el permiso "Publicar contenido" en alguna categoria
    :param user: usuario a comprobar (User)
    :return: True tiene el permiso, False en caso contrario (Boolean)
    """
    return user.tiene_permiso_publicar_contenido()

def tiene_permiso_crear_o_editar_contenido(user):
    """
    Funcion que comprueba si el usuario tiene el permiso "Crear contenido" o "Editar contenido" en alguna categoria
    :param user: usuario a comprobar (User)
    :return: True tiene el permiso, False en caso contrario (Boolean)
    """
    return user.tiene_permiso_crear_contenido() or user.tiene_permiso_editar_contenido()

@login_required
@user_passes_test(tiene_permiso_crear_contenido)
def crearContenido(request):
    """
    Vista para crear nuevo contenido. Requiere autenticación.
    Args:
        request: Objeto de solicitud HTTP.
    Returns:
        HttpResponse: Respuesta HTTP que redirige a la lista de contenidos o muestra el formulario de creación.
    """
    categorias_autor = UserCategoria.objects.filter(user=request.user, rol__nombre='Autor').values_list('categoria__id', flat=True)

    if request.method == 'POST':

        form = ContenidoForm(request.POST, autor=request.user, categorias_autor=categorias_autor)
        form.autor = request.user
        
        if form.is_valid():
            contenido = form.save(commit=False)
            contenido.autor = request.user
            contenido.tipo_contenido = form.cleaned_data['tipo_contenido']
            contenido.save()
            return redirect('contenido:lista_contenido')
    else:
        form = ContenidoForm(categorias_autor=categorias_autor, autor=request.user)
    
    return render(request, 'contenido/crearContenido.html', {'form': form})

@login_required
@user_passes_test(tiene_permiso_crear_o_editar_contenido)
def editarContenido(request, id):
    """
    Vista para editar contenido existente. Requiere autenticación.
    Args:
        request: Objeto de solicitud HTTP.
        id (int): ID del contenido a editar.
    Returns:
        HttpResponse: Respuesta HTTP que redirige a la lista de contenidos o muestra el formulario de edición.
    """
    contenido = get_object_or_404(Contenido, id=id)
    if (request.user).is_autor_in_categoria(contenido.categoria):
        categorias_autor = UserCategoria.objects.filter(user=request.user, rol__nombre='Autor').values_list('categoria__id', flat=True)
    else:
        categorias_autor = Contenido.objects.filter(id=id).values_list('categoria__id', flat=True)
    if request.method == 'POST':
        if (request.user).is_autor_in_categoria(contenido.categoria):
            form = ContenidoForm(request.POST, instance=contenido, autor=request.user, categorias_autor=categorias_autor)
        else:
            form = EditorContenidoForm(request.POST, instance=contenido)
        if form.is_valid():
            if (request.user).is_autor_in_categoria(contenido.categoria):
                contenido.tipo_contenido = form.cleaned_data['tipo_contenido']
            form.save()
            if (request.user).is_autor_in_categoria(contenido.categoria):
                return redirect('contenido:lista_contenido')
            else:
                return redirect('contenido:lista_editor')
    else:
        if (request.user).is_autor_in_categoria(contenido.categoria):
            form = ContenidoForm(instance=contenido, categorias_autor=categorias_autor, autor=request.user)
        else:
            form = EditorContenidoForm(instance=contenido)
    return render(request, 'contenido/editarContenido.html', {'form': form})

@login_required
@user_passes_test(tiene_permiso_eliminar_contenido)
def eliminarContenido(request, id):
    """
    Vista para eliminar contenido existente. Requiere autenticación.
    Args:
        request: Objeto de solicitud HTTP.
        id (int): ID del contenido a eliminar.
    Returns:
        HttpResponse: Respuesta HTTP que redirige a la lista de contenidos.
    """
    contenido = get_object_or_404(Contenido, id=id)
    contenido.delete()
    return redirect('contenido:lista_contenido')

@login_required
@user_passes_test(tiene_permiso_eliminar_contenido)
def confirmarEliminarContenido(request, id):
    """
    Vista para confirmar la eliminación de un contenido existente. Requiere autenticación.
    Args:
        request: Objeto de solicitud HTTP.
        id (int): ID del contenido a confirmar la eliminación.
    Returns:
        HttpResponse: Respuesta HTTP que muestra la página de confirmación de eliminación.
    """
    contenido = get_object_or_404(Contenido, id=id)
    return render(request, 'contenido/confirmarEliminarContenido.html', {'contenido': contenido})

@login_required
@user_passes_test(tiene_permiso_crear_contenido)
def listaContenido(request):
    """
    Vista para listar los contenidos de un usuario
    :param request: Objeto de solicitud HTTP.
    :return: HttpResponse: Respuesta HTTP que muestra la lista de contenidos.
    """
    user = User.objects.get(id=request.user.id)
    contenido = Contenido.for_user(user)
    #contenido = contenido.filter(estado='Borrador')
    return render(request, 'contenido/listaContenido.html', {'contenidos': contenido})

def verContenido(request, id):
    """
    Vista para ver un contenido específico. No requiere autenticación.
    Args:
        request: Objeto de solicitud HTTP.
        id (int): ID del contenido a visualizar.
    Returns:
        HttpResponse: Respuesta HTTP que muestra la página del contenido específico.
    """
    contenido = Contenido.objects.get(id=id)
    contenido.numero_vistas += 1
    contenido.save()
    
    return render(request, 'contenido/verContenido.html', {'contenido': contenido})

def listaTodos(request):
    """
    Vista para mostrar la lista de contenidos de todos los usuarios.
    :param request: Objeto de solicitud HTTP.
    :return: HttpResponse: Respuesta HTTP que muestra la lista de contenidos.
    """
    contenido = Contenido.objects.all()
    contenido = contenido.filter(estado='Publicado')
    categorias = Categoria.objects.all()
    tipos_contenido = tipoContenido.objects.all()

    if request.user and request.user.is_authenticated:
        usuario = User.objects.get(id=request.user.id)
        if usuario and usuario.tiene_permiso_deshabilitar_contenido():
            categorias_deshabilitar = usuario.obtener_categorias_por_permiso('Deshabilitar contenido')
        else:
            categorias_deshabilitar = []
    else:
        categorias_deshabilitar = []
        
    return render(request, 'contenido/listaTodos.html', {'contenidos': contenido, 'categorias': categorias, 'tipos_contenido': tipos_contenido, 'categorias_deshabilitar': categorias_deshabilitar})

@login_required
@user_passes_test(tiene_permiso_publicar_contenido)
def listaPublicador(request):

    """
    Vista para mostrar la lista de contenidos de los usuarios publicadores.
    :param request: Objeto de solicitud HTTP.
    :return: HttpResponse: Respuesta HTTP que muestra la lista de contenidos.
    """

    user = User.objects.get(id=request.user.id)
    categorias = UserCategoria.objects.filter(user=user, rol__nombre='Publicador').values_list('categoria__id', flat=True)
    contenido = Contenido.for_categorias(categorias)
    contenido = contenido.filter(estado='Publicacion')
    return render(request, 'contenido/listaPublicador.html', {'contenidos': contenido})

@login_required
@user_passes_test(tiene_permiso_editar_contenido)
def listaEditor(request):
    """
    Vista para mostrar la lista de contenidos de los usuarios editores.
    :param request: Objeto de solicitud HTTP.
    :return: HttpResponse: Respuesta HTTP que muestra la lista de contenidos.
    """
    user = User.objects.get(id=request.user.id)
    categorias = UserCategoria.objects.filter(user=user, rol__nombre='Editor').values_list('categoria__id', flat=True)
    contenido = Contenido.for_categorias(categorias)
    contenido = contenido.filter(estado='Edicion')
    return render(request, 'contenido/listaEditor.html', {'contenidos': contenido})

@login_required
def valorarContenido(request, id):
    """
    Vista para valorar un contenido específico. Requiere autenticación.
    Args:
        request: Objeto de solicitud HTTP.
        id (int): ID del contenido a valorar.
    Returns:
        HttpResponse: Redirige a la página del contenido valorado o muestra un mensaje de error.
    """
    if request.method == 'POST':
        contenido = get_object_or_404(Contenido, id=id)
        puntuacion = int(request.POST.get('puntuacion'))  # Asume que tienes un formulario con un campo 'puntuacion'

        # Comprueba si el usuario ya ha valorado este contenido
        valoracion_existente = Valoracion.objects.filter(contenido=contenido, usuario=request.user).first()
        if valoracion_existente:
            # Actualiza la valoración si el usuario ya ha valorado este contenido
            valoracion_existente.puntuacion = puntuacion
            valoracion_existente.save()
        else:
            # Crea una nueva valoración si el usuario no ha valorado este contenido
            valoracion = Valoracion(contenido=contenido, usuario=request.user, puntuacion=puntuacion)
            valoracion.save()

        # Recalcula la puntuación promedio del contenido y el número de valoraciones
        valoraciones = Valoracion.objects.filter(contenido=contenido)
        total_puntuacion = sum(valoracion.puntuacion for valoracion in valoraciones)
        numero_valoraciones = valoraciones.count()
        contenido.puntuacion = total_puntuacion / numero_valoraciones
        contenido.numero_valoraciones = numero_valoraciones
        contenido.save()

        return redirect('contenido:ver_contenido', id=id)
    else:
        # Muestra el contenido específico para que el usuario pueda valorarlo
        contenido = get_object_or_404(Contenido, id=id)
        return render(request, 'contenido/valorarContenido.html', {'contenido': contenido})

def buscarContenido(request):
    """
    Vista para buscar contenidos por título de contenido o nombre de categoría.
    Args:
        request: Objeto de solicitud HTTP.
    Returns:
        HttpResponse: Respuesta HTTP que muestra los resultados de la búsqueda.
    """
    query = request.GET.get('q')

    contenidos = Contenido.objects.filter(
        Q(titulo__icontains=query) |
        Q(categoria__nombre__icontains=query) |
        Q(autor__first_name__icontains=query) |
        Q(autor__last_name__icontains=query)
    )

    return render(request, 'contenido/listaTodos.html', {'contenidos': contenidos, 'categorias': Categoria.objects.all()})

@login_required
@user_passes_test(tiene_permiso_crear_contenido)
def aEdicion(request, id):
    """
    Función que sirve para cambiar el estado de un contenido a "Edicion"
    :param request: Objeto de solicitud HTTP.
    :id: id del contenido a cambiar de estado
    :return: HttpResponse: Respuesta HTTP que muestra la lista de contenidos.
    """
    contenido = Contenido.objects.get(id=id)
    contenido.estado = 'Edicion'
    contenido.save()

    # Notificar a los usuarios editores en la categoría del contenido
    categoria = contenido.categoria  # Obtener la categoría del contenido
    users_with_editor_role = User.objects.filter(
        usercategoria__rol__nombre="Editor",
        usercategoria__categoria=categoria
    )
    #print(contenido)
    new_notifications = []
    for user in users_with_editor_role:
        notification = notificar.send(sender=contenido.autor, verb=contenido.titulo, destiny=user, timestamp=timezone.now(),categoria_destino=categoria,tipo_accion='Edicion')
        new_notifications.extend(notification)


    user = User.objects.get(id=request.user.id)
    contenido = Contenido.for_user(user)
    #contenido = contenido.filter(estado='Borrador')
    return render(request, 'contenido/listaContenido.html', {'contenidos': contenido})

@login_required
@user_passes_test(tiene_permiso_editar_contenido)
def aPublicacion(request, id):
    """
    Función que sirve para cambiar el estado de un contenido a "Publicacion"
    :param request: Objeto de solicitud HTTP.
    :id: id del contenido a cambiar de estado
    :return: HttpResponse: Respuesta HTTP que muestra la lista de contenidos.
    """
    contenido = Contenido.objects.get(id=id)
    contenido.estado = 'Publicacion'
    contenido.save()

    # Notificar a los usuarios publicadores en la categoría del contenido
    categoria = contenido.categoria  # Obtener la categoría del contenido
    users_with_publicador_role = User.objects.filter(
        usercategoria__rol__nombre="Publicador",
        usercategoria__categoria=categoria
    )

    new_notifications = []
    for user in users_with_publicador_role:
        notification = notificar.send(sender=contenido.autor, verb=contenido.titulo, destiny=user,
                                      timestamp=timezone.now(), categoria_destino=categoria, tipo_accion='Publicacion')
        new_notifications.extend(notification)


    user = User.objects.get(id=request.user.id)
    categorias = UserCategoria.objects.filter(user=user, rol__nombre='Editor').values_list('categoria__id', flat=True)
    contenido = Contenido.for_categorias(categorias)
    contenido = contenido.filter(estado='Edicion')
    return render(request, 'contenido/listaEditor.html', {'contenidos': contenido})

@login_required
@user_passes_test(tiene_permiso_publicar_contenido)
def publicarContenido(request, id):
    """
    Función que sirve para cambiar el estado de un contenido a "Publicado"
    :param request: Objeto de solicitud HTTP.
    :id: id del contenido a cambiar de estado
    :return: HttpResponse: Respuesta HTTP que muestra la lista de contenidos.
    """
    contenido = Contenido.objects.get(id=id)
    contenido.estado = 'Publicado'
    contenido.save()

    user = User.objects.get(id=request.user.id)
    categorias = UserCategoria.objects.filter(user=user, rol__nombre='Publicador').values_list('categoria__id', flat=True)
    contenido = Contenido.for_categorias(categorias)
    contenido = contenido.filter(estado='Publicacion')
    return render(request, 'contenido/listaPublicador.html', {'contenidos': contenido})

@login_required
@user_passes_test(tiene_permiso_visualizar_kanban)
def kanbanView(request):
    """
    Vista de Kanban para mostrar contenidos organizados por categoría y estado.
    Esta vista recopila todos los contenidos de la base de datos y los organiza en un tablero Kanban.
    Los contenidos se agrupan por categoría y estado para su visualización.
    Args:
        request (HttpRequest): La solicitud HTTP que desencadenó esta vista.
    Returns:
        HttpResponse: Una respuesta HTTP que renderiza la plantilla 'contenido/kanban.html' con
        los contenidos organizados en forma de tablero Kanban.
    Raises:
        N/A
    Example:
        Ejemplo de uso en una URL de Django:
        ```
        path('kanban/', views.kanbanView, name='kanban'),
        ```
    """
    # Obtén todos los contenidos de tu base de datos
    contenidos = Contenido.objects.all()

    # Organiza los contenidos en un diccionario por categoría y estado
    tablero_kanban = {}

    for contenido in contenidos:
        categoria = contenido.categoria.nombre
        estado = contenido.estado

        if categoria not in tablero_kanban:
            tablero_kanban[categoria] = {}

        if estado not in tablero_kanban[categoria]:
            tablero_kanban[categoria][estado] = []

        tablero_kanban[categoria][estado].append(contenido)

    return render(request, 'contenido/kanban.html', {'tablero_kanban': tablero_kanban})

login_required
@user_passes_test(tiene_permiso_visualizar_kanban)
def reportesView(request):
    """
    Vista de Reportes para mostrar reportes de datos de la aplicación.
    Esta vista recopila todos los datos de la base de datos y los organiza en un reporte.
    Los datos se agrupan por categoría y estado para su visualización.
    Args:
        request (HttpRequest): La solicitud HTTP que desencadenó esta vista.
    Returns:
        HttpResponse: Una respuesta HTTP que renderiza la plantilla 'contenido/reportes.html' con
        los datos organizados en forma de reporte.
    Raises:
        N/A
    Example:
        Ejemplo de uso en una URL de Django:
        ```
        path('reportes/', views.reportesView, name='reportes'),
        ```
    """
    # Obtén todos los contenidos de tu base de datos
    contenidos = Contenido.objects.all()
    # Reporte 1: Genera un reporte del numero de contenido por categoria
    reporte1 = {}
    reporte_contenidos_por_categoria = defaultdict(list)
    for contenido in contenidos:
        if contenido.estado == 'Publicado':
            categoria = contenido.categoria.nombre
            if categoria not in reporte1:
                reporte1[categoria] = 0
            reporte1[categoria] += 1
            reporte_contenidos_por_categoria[categoria].append(contenido.titulo)

    
    # Genera un gráfico de pastel
    df = pd.DataFrame.from_dict(reporte1, orient='index', columns=['Cantidad'])
    plt.figure(figsize=(8, 8))
    plt.pie(df['Cantidad'], labels=df.index, autopct='%1.1f%%', startangle=90)
    plt.title('Número de Contenidos por Categoría')
    plt.axis('equal')  # Asegura que el gráfico de pastel sea un círculo.
    
    # Convierte el gráfico en una imagen para mostrar en el HTML
    img_data = BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    img_base64 = base64.b64encode(img_data.read()).decode()
    img_src1 = f'data:image/png;base64,{img_base64}'

    #Reporte 2: Genera un reporte del promedio de puntuacion por categoria
    reporte2 = {}
    for contenido in contenidos:
        categoria = contenido.categoria.nombre
        if categoria not in reporte2:
            reporte2[categoria] = 0
        reporte2[categoria] += contenido.puntuacion
    for categoria in reporte2:
        reporte2[categoria] = reporte2[categoria] / reporte1[categoria]
    
    # Reporte 3: Genera un reporte del contenido mas valorado por categoria
    reporte3 = {}
    for contenido in contenidos:
        categoria = contenido.categoria.nombre
        if categoria not in reporte3:
            reporte3[categoria] = 0
        reporte3[categoria] = max(reporte3[categoria], contenido.puntuacion)
    
    # Reporte 4: Genera un reporte del contenido del promedio de vistas por categoria
    reporte4 = {}
    for contenido in contenidos:
        categoria = contenido.categoria.nombre
        if categoria not in reporte4:
            reporte4[categoria] = 0
        reporte4[categoria] += contenido.numero_vistas


    #return
    return render(request, 'contenido/reportes.html', {'reporte1': reporte1,'img_src1': img_src1,'reporte_contenidos_por_categoria': dict(reporte_contenidos_por_categoria),
                                                        'reporte2': reporte2,'reporte3': reporte3,'reporte4': reporte4,
                                                        'reporte3_contenidos_por_categoria': dict(reporte_contenidos_por_categoria),
                                                        'reporte4_contenidos_por_categoria': dict(reporte_contenidos_por_categoria)
                                                        })



@login_required
@user_passes_test(tiene_permiso_publicar_contenido)
def rechazar_contenido(request, id):
    """
    Función que sirve para cambiar el estado de un contenido a "Rechazado"
    :param request: Objeto de solicitud HTTP.
    :id: id del contenido a cambiar de estado
    :return: HttpResponse: Respuesta HTTP que muestra la lista de contenidos.
    """
    contenido = Contenido.objects.get(id=id)
    contenido.estado = 'Rechazado'
    contenido.save()

    user = User.objects.get(id=request.user.id)
    categorias = UserCategoria.objects.filter(user=user, rol__nombre='Publicador').values_list('categoria__id', flat=True)
    contenido = Contenido.for_categorias(categorias)
    contenido = contenido.filter(estado='Publicacion')
    return render(request, 'contenido/listaPublicador.html', {'contenidos': contenido})

def deshabilitar_contenido(request, id):
    """
    Función que sirve para cambiar el estado de un contenido a "Deshabilitado"
    :param request: Objeto de solicitud HTTP.
    :id: id del contenido a cambiar de estado
    :return: HttpResponse: Respuesta HTTP que muestra la lista de contenidos.
    """
    contenido = Contenido.objects.get(id=id)
    contenido.estado = 'Deshabilitado'
    contenido.save()
    return redirect('contenido:lista_todos')