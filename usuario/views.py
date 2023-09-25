# Create your views here.
from .models import User
from django.shortcuts import render

def verUsuarios(request):
    usuarios = User.objects.all()
    return render(request, 'account/verUsuarios.html', {'usuarios': usuarios})
