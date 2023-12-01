from django import forms
from .models import UserCategoria
from .models import Rol

class UserCategoriaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user_rol = kwargs.pop('user_rol', None)
        super(UserCategoriaForm, self).__init__(*args, **kwargs)

        # Filtra el queryset del campo 'rol' según el rol del usuario
        if user_rol != "Administrador":
            roles_disponibles = Rol.objects.exclude(permisos__nombre="Asignar roles").distinct().order_by('id')
            self.fields['rol'].queryset = roles_disponibles

    class Meta:

        model = UserCategoria
        # Excluimos el campo user para que no se muestre en el formulario
        exclude = ['user', 'categoria']
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