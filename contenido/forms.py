from django import forms
from .models import Contenido

class ContenidoForm(forms.ModelForm):
    class Meta:
        model = Contenido
        fields = ['titulo', 'cuerpo', 'autor', 'categoria']
        labels = {
            'titulo': 'Titulo',
            'cuerpo': 'Cuerpo',
            'autor': 'Autor',
            'categoria': 'Categoria',
        }
        widgets = {
            'cuerpo': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }