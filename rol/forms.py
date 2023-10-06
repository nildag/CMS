from django import forms
from .models import Rol
from permiso.models import Permiso

class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ['nombre', 'descripcion', 'permisos']
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripcion',
            'permisos': 'Permisos',
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'permisos': forms.CheckboxSelectMultiple(),
        }