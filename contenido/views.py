from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.urls import reverse

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
import numpy as np

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
            # Registrar el cambio
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(contenido).id,
                object_id=contenido.id,
                object_repr=str(contenido),
                action_flag=ADDITION,
            )

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

            # Registrar el cambio
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(contenido).id,
                object_id=contenido.id,
                object_repr=str(contenido),
                action_flag=CHANGE,
            )

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
    if contenido.estado == 'Publicado':
        contenido.numero_vistas += 1
    contenido.save()

    historial_url = reverse('contenido:historial_cambios', args=[contenido.id])

    return render(request, 'contenido/verContenido.html', {'contenido': contenido, 'historial_url':historial_url})

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

@login_required
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
    # Reporte 1: Número de contenidos por categoría con gráfico de pastel
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

    #Reporte 2: Genera un reporte del promedio de puntuacion de todos los contenidos de cada categoria
    """
    reporte2 = {}
    for contenido in contenidos:
        categoria = contenido.categoria.nombre
        if categoria not in reporte2:
            reporte2[categoria] = 0
        reporte2[categoria] += contenido.puntuacion
    for categoria in reporte2:
        reporte2[categoria] = reporte2[categoria] / reporte1[categoria]
    """

    reporte2 = {}
    for contenido in contenidos:
        categoria = contenido.categoria.nombre
        if categoria not in reporte2:
            reporte2[categoria] = {'total_puntuacion': 0, 'numero_contenidos': 0}
        reporte2[categoria]['total_puntuacion'] += contenido.puntuacion
        reporte2[categoria]['numero_contenidos'] += 1

    #calcula el promedio de puntuacion de cada categoria
    promedio_puntuacion_por_categoria = {}
    for categoria in reporte2:
        promedio_puntuacion_por_categoria[categoria] = reporte2[categoria]['total_puntuacion'] / reporte2[categoria]['numero_contenidos']
    
    # Genera un los indices para el grafico de barras
    categorias = list(promedio_puntuacion_por_categoria.keys())
    promedios = list(promedio_puntuacion_por_categoria.values())

    # Genera un gráfico de barras
    fig, ax = plt.subplots(figsize=(8, 8))
    anchobarra = 0.30
    barras = ax.bar(categorias, promedios,anchobarra)

    for barra in barras:
        altura = barra.get_height()
        ax.text(barra.get_x() + barra.get_width() / 2, altura, f'{altura:.2f}', ha='center', va='bottom')

    ax.set_title('Promedio de Puntuación por Categoría')
    ax.set_xlabel('Categoría')
    ax.set_ylabel('Promedio de Puntuación')
    ax.set_xticklabels(categorias, rotation=45, ha='right')
    ax.set_ylim(0, 5)
    ax.set_yticks([0, 1, 2, 3, 4, 5])
    ax.grid(True)
    fig.tight_layout()

    # Mostrar el grafico de barras
    plt.tight_layout()
    plt.show()

    # Convierte el gráfico en una imagen para mostrar en el HTML
    img_data = BytesIO()
    fig.savefig(img_data, format='png')
    img_data.seek(0)
    img_base64 = base64.b64encode(img_data.read()).decode()
    img_src2 = f'data:image/png;base64,{img_base64}'


    # Reporte 3: Genera un reporte del contenido mejor valorado por categoria
    reporte3 = {}
    for contenido in contenidos:
        categoria = contenido.categoria.nombre
        if categoria not in reporte3:
            reporte3[categoria] = 0
        reporte3[categoria] = max(reporte3[categoria], contenido.puntuacion)
    
    # Reporte 4: Cantidad total de vistas de los contenidos de cada categoría
    reporte4 = {}
    for contenido in contenidos:
        categoria = contenido.categoria.nombre
        if categoria not in reporte4:
            reporte4[categoria] = 0
        reporte4[categoria] += contenido.numero_vistas

    # Reporte 5: Rendimiento de los contenidos del Autor
    """ -Promedio de valoraciones de todos sus contenidos publicados
    -Titulo, categoría, cantidad de vistas, fecha y valoración de su contenido más valorado/popular
    -Titulo, categoría, cantidad de vistas, fecha y valoración de su contenido menos valorado/popular    
    """
    reporte5 = {}

    for user in User.objects.all():
        usuario=user.email
        reporte5[usuario] = {'total_puntuacion': 0, 'numero_contenidos': 0,
                         'mejor_valorado': {'titulo': '', 'categoria': '', 'cantidad_vistas': 0, 'fecha': '', 'valoracion': float('-inf')},
                         'peor_valorado': {'titulo': '', 'categoria': '', 'cantidad_vistas': 0, 'fecha': '', 'valoracion': float('inf')}}

        for contenido in contenidos:
            if contenido.autor == user and contenido.estado == 'Publicado':
                if usuario not in reporte5:
                    reporte5[usuario] = {'total_puntuacion': 0, 'numero_contenidos': 0, 'mejor_valorado': {'titulo': '', 'categoria': '', 'cantidad_vistas': 0, 'fecha': '', 'valoracion': float('-inf')}, 'peor_valorado': {'titulo': '', 'categoria': '', 'cantidad_vistas': 0, 'fecha': '', 'valoracion': float('inf')}}
                reporte5[usuario]['total_puntuacion'] += contenido.puntuacion
                reporte5[usuario]['numero_contenidos'] += 1
                if contenido.puntuacion > reporte5[usuario]['mejor_valorado']['valoracion']:
                    # Actualiza el mejor valorado
                    reporte5[usuario]['mejor_valorado']['titulo'] = contenido.titulo
                    reporte5[usuario]['mejor_valorado']['categoria'] = contenido.categoria.nombre
                    reporte5[usuario]['mejor_valorado']['cantidad_vistas'] = contenido.numero_vistas
                    reporte5[usuario]['mejor_valorado']['fecha'] = contenido.fecha_creacion
                    reporte5[usuario]['mejor_valorado']['valoracion'] = contenido.puntuacion

                if contenido.puntuacion < reporte5[usuario]['peor_valorado']['valoracion']:
                    # Actualiza el peor valorado
                    reporte5[usuario]['peor_valorado']['titulo'] = contenido.titulo
                    reporte5[usuario]['peor_valorado']['categoria'] = contenido.categoria.nombre
                    reporte5[usuario]['peor_valorado']['cantidad_vistas'] = contenido.numero_vistas
                    reporte5[usuario]['peor_valorado']['fecha'] = contenido.fecha_creacion
                    reporte5[usuario]['peor_valorado']['valoracion'] = contenido.puntuacion

    #calcula el promedio de puntuacion de cada autor
    promedio_puntuacion_por_autor = {}
    for usuario in reporte5:
        total_puntuacion = reporte5[usuario]['total_puntuacion']
        numero_contenidos = reporte5[usuario]['numero_contenidos']

        # Verificación para evitar la división por cero
        promedio_puntuacion_por_autor[usuario] = total_puntuacion / numero_contenidos if numero_contenidos != 0 else 0

    # Filtra solo los usuarios que tienen contenido
    usuarios_con_contenido = [usuario for usuario in promedio_puntuacion_por_autor.keys() if promedio_puntuacion_por_autor[usuario] != 0]
    usuarios = list(map(str, usuarios_con_contenido))
    promedios = [promedio_puntuacion_por_autor[usuario] for usuario in usuarios_con_contenido]
    mejor_valorado = [reporte5[usuario]['mejor_valorado']['valoracion'] for usuario in usuarios_con_contenido]
    peor_valorado = [reporte5[usuario]['peor_valorado']['valoracion'] for usuario in usuarios_con_contenido]


    # Genera un gráfico de barras
    fig, ax = plt.subplots(figsize=(8, 8))
    columnas = np.arange(len(usuarios))
    anchobarra = 0.20

    # Lista para almacenar las alturas de las barras para el contenido mejor valorado y peor valorado
    alturas_mejor_valorado = []
    alturas_peor_valorado = []

    for usuario in usuarios:
        alturas_mejor_valorado.append(reporte5[usuario]['mejor_valorado']['valoracion'])
        alturas_peor_valorado.append(reporte5[usuario]['peor_valorado']['valoracion'])

    # Llena con ceros para los autores que no tienen información de mejor o peor valorado
    alturas_mejor_valorado = [0 if valor is None else valor for valor in alturas_mejor_valorado]
    alturas_peor_valorado = [0 if valor is None else valor for valor in alturas_peor_valorado]

    #grafico de barras para el contenido mejor valorado
    ax.bar(columnas - anchobarra, alturas_mejor_valorado, anchobarra, label='Mejor Valorado', color='green')
    
    #grafico de barras para el contenido peor valorado
    ax.bar(columnas, alturas_peor_valorado, anchobarra, label='Peor Valorado', color='red')

    
    ax.set_title('Contenido con mejor/peor promedio de valoraciones por autor')
    ax.set_xlabel('Autor')
    ax.set_ylabel('Promedio de Puntuación')
    ax.set_xticks(columnas - anchobarra / 2)
    ax.set_xticklabels(usuarios, rotation=45, ha='right', rotation_mode='anchor')
    ax.legend()
    ax.set_ylim(0, 5)
    ax.set_yticks([0, 1, 2, 3, 4, 5])
    ax.grid(True)
    fig.tight_layout()
    
    # Mostrar el grafico de barras
    plt.tight_layout()
    plt.show()

    # Convierte el gráfico en una imagen para mostrar en el HTML
    img_data = BytesIO()
    fig.savefig(img_data, format='png')
    img_data.seek(0)
    img_base64 = base64.b64encode(img_data.read()).decode()
    img_src5 = f'data:image/png;base64,{img_base64}'

   
    #return
    return render(request, 'contenido/reportes.html', {'reporte1': reporte1, 'img_src1': img_src1,'reporte_contenidos_por_categoria': dict(reporte_contenidos_por_categoria),
                                                        'reporte2': reporte2, 'img_src2': img_src2, 'promedio_puntuacion_por_categoria': promedio_puntuacion_por_categoria,
                                                        'reporte3': reporte3,  
                                                        'reporte4': reporte4,
                                                        'reporte5': reporte5, 'img_src5': img_src5, 'promedio_puntuacion_por_autor': promedio_puntuacion_por_autor
                                                        
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

def historialCambiosContenido(request, id):
    contenido = get_object_or_404(Contenido, id=id)
    historial_cambios = LogEntry.objects.filter(
        content_type_id=ContentType.objects.get_for_model(contenido).id,
        object_id=contenido.id
    )

    return render(request, 'contenido/historialCambiosContenido.html', {'contenido': contenido, 'historial_cambios': historial_cambios})

@login_required
@user_passes_test(tiene_permiso_editar_contenido)
def historial_cambios(request, contenido_id):
    contenido = get_object_or_404(Contenido, id=contenido_id)
    historial_cambios = LogEntry.objects.filter(
        content_type__app_label='contenido',
        content_type__model='contenido',
        object_id=contenido_id
    )

    return render(request, 'contenido/historialCambiosContenido.html', {'contenido': contenido, 'historial_cambios': historial_cambios})
