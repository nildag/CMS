from django import forms
from .models import Contenido
from categorias.models import Categoria
from usuario.models import UserCategoria
from tipoContenido.models import tipoContenido

class ContenidoForm(forms.ModelForm):
    """
    Formulario para crear o editar contenido.

    Atributos:
        autor (User): Usuario que crea o edita el contenido.
        categorias_autor (QuerySet): Categorías asociadas al autor.
    """
    class Meta:
        model = Contenido
        fields = ['titulo', 'cuerpo', 'categoria', 'tipo_contenido']
        labels = {
            'titulo': 'Titulo',
            'cuerpo': 'Cuerpo',
            'categoria': 'Categoria',
            'tipo_c ontenido': 'Tipo de Contenido'
        }
        widgets = {
            'cuerpo': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'autor': forms.HiddenInput() 
        }

    def __init__(self, *args, **kwargs):
        """
        Inicializa el formulario con datos específicos del autor y sus categorías asociadas.

        Args:
            autor (User): Usuario que crea o edita el contenido.
            categorias_autor (QuerySet): Categorías asociadas al autor.
        """
        autor = kwargs.pop('autor', None)
        categorias_autor = kwargs.pop('categorias_autor', None)
        super(ContenidoForm, self).__init__(*args, **kwargs)

        if autor is not None:
            self.initial['autor'] = autor

        if categorias_autor is not None:
            self.fields['categoria'].queryset = Categoria.objects.filter(id__in=categorias_autor)
