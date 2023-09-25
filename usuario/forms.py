from django import forms
from .models import UserCategoria


class UserCategoriaForm(forms.ModelForm):

    class Meta:

        model = UserCategoria
        # Excluimos el campo user para que no se muestre en el formulario
        exclude = ['user']
        fields = [
            'user',
            'categoria',
            'rol',
        ]
        labels = {
            'user': 'Usuario',
            'categoria': 'Categoria',
            'rol': 'Rol',
        }
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
        }
