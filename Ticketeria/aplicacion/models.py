from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    nombre = models.CharField(max_length=20)
    email = models.EmailField()
    phoneNumber = models.IntegerField()
    direccion = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.nombre}"

class Compra(models.Model):
    producto = models.CharField(max_length=20)
    codigo = models.IntegerField()
    cantidad = models.IntegerField()    
    
    def __str__(self):
        return f"{self.producto}, {self.codigo}"
    
class Artista(models.Model):
    nombreArtista = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=500)
    
    def __str__(self):
        return f"{self.nombreArtista}"
    
class ProximaFecha(models.Model):
    artista = models.CharField(max_length=20)
    date = models.DateTimeField()
    lugar = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=100, default="La música existe para cuando nos fallan las palabras.")
    img = models.ImageField(upload_to="avatares", default="../media/imagenes/concierto.jpg")
    
    def __str__(self):
        return f"{self.artista}"
    
class Avatar(models.Model):
    imagen = models.ImageField(upload_to="avatares")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user} {self.imagen}"