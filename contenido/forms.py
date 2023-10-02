from django import forms
from .models import Contenido
from categorias.models import Categoria
from usuario.models import UserCategoria

class ContenidoForm(forms.ModelForm):
    class Meta:
            model = Contenido
            fields = ['titulo', 'cuerpo', 'categoria']
            labels = {
                'titulo': 'Titulo',
                'cuerpo': 'Cuerpo',
                'categoria': 'Categoria',
            }
            widgets = {
                'cuerpo': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
                 'autor': forms.HiddenInput() 
            }

    def __init__(self, *args, **kwargs):
        autor = kwargs.pop('autor', None)
        categorias_autor = kwargs.pop('categorias_autor', None)
        super(ContenidoForm, self).__init__(*args, **kwargs)

        if autor is not None:
            self.initial['autor'] = autor

        if categorias_autor is not None:
            self.fields['categoria'].queryset = Categoria.objects.filter(id__in=categorias_autor)