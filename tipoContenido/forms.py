from django import forms
from .models import tipoContenido

class tipoContenidoForm(forms.ModelForm):
    class Meta:
        model = tipoContenido
        fields = ['nombre', 'descripcion']
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripcion',
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }