from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class PerfilForm(forms.Form):
    nombre = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)
    phoneNumber = forms.IntegerField(required=True)
    direccion = forms.CharField(max_length=50, required=True)
    
class CompraForm(forms.Form):
    producto = forms.CharField(max_length=20, required=True)
    codigo = forms.IntegerField(required=True)
    cantidad = forms.IntegerField(required=True)
    
class ArtistaForm(forms.Form):
    nombreArtista = forms.CharField(max_length=20, required=True)
    descripcion = forms.CharField(max_length=500, required=True)
    
class ProximaFechaForm(forms.Form):
    artista = forms.CharField(max_length=20, required=True)
    date = forms.DateTimeField(required=True)
    lugar = forms.CharField(max_length=20, required=True)
    descripcion = forms.CharField(max_length=100, required=True)
    img = forms.ImageField(required=True)
    
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar Contraseña", widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        
class UserEditForm(UserChangeForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label="Nombre/s", max_length=50, required=True)
    last_name = forms.CharField(label="Apellido/s", max_length=50, required=True)
    
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]
    
class AvatarForm(forms.Form):
    imagen = forms.ImageField(required=True)