from django import forms
from .models import Categoria

class CategoriaForm(forms.ModelForm):
    """
    Clase de formulario para la creación y edición de categorías.

    Atributos:
    - model (Categoria): El modelo de datos subyacente para el formulario.
    - fields (list): Lista de campos del modelo que se deben mostrar en el formulario.
    - labels (dict): Etiquetas personalizadas para los campos del formulario.
    - widgets (dict): Configuración personalizada de widgets para los campos del formulario.

    Ejemplo:
    model = Categoria
    fields = ['nombre', 'descripcion']
    labels = {
        'nombre': 'Nombre',
        'descripcion': 'Descripcion',
    }
    widgets = {
        'descripcion': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
    }
    """
    class Meta:
        """
        Metaclase que proporciona metadatos para el formulario.

        Atributos:
        - model (Categoria): El modelo de datos subyacente para el formulario.
        - fields (list): Lista de campos del modelo que se deben mostrar en el formulario.
        - labels (dict): Etiquetas personalizadas para los campos del formulario.
        - widgets (dict): Configuración personalizada de widgets para los campos del formulario.
        """
        model = Categoria
        fields = ['nombre', 'descripcion']
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripcion',
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
