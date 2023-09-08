from django.db import models

class Categoria(models.Model):
    #atributos de la clase
    descripcion = models.CharField(max_length=255)

    #Metodo para obtener la categoria
    def getCategoria(self):
        return self

    #Metodo para establecer la nueva categoria
    def setCategoria(self, nuevaDescripcion):
        self.descripcion = nuevaDescripcion
        self.save()

    #Metodo para obtener la descripcion
    def getDescripcion(self):
        return self.descripcion

    #Metodo para establecer la descripcion
    def setDescripcion(self, nuevaDescripcion):
        self.descripcion = nuevaDescripcion
        self.save()

    @classmethod
    def crearCateggoria(cls,descripcion):
        nuevaCategoria = cls(descripcion=descripcion)
        nuevaCategoria.save()
        return nuevaCategoria

    def __str__(self):
        return f"{self.id}: {self.descripcion}"
