from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views.generic import UpdateView

from .models import *
from .forms import *

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordChangeView

from django.http import HttpResponseNotAllowed

from django.contrib.auth.mixins import LoginRequiredMixin #Clase
from django.contrib.auth.decorators import login_required #Funcion


def home(request):
    return render(request, "aplicacion/index.html")

#------------- Perfil ---------------------
@login_required
def perfil(request):
    contexto = { 'perfil': Perfil.objects.all() }
    return render(request, "aplicacion/perfil.html", contexto)

@login_required
def perfilCreate(request):
    if request.method == "POST":
        miForm = PerfilForm(request.POST)
        if miForm.is_valid():
            perfil_nombre = miForm.cleaned_data.get("nombre")
            perfil_email = miForm.cleaned_data.get("email")
            perfil_phoneNumber = miForm.cleaned_data.get("phoneNumber")
            perfil_direccion = miForm.cleaned_data.get("direccion")
            perfil = Perfil(nombre=perfil_nombre, email=perfil_email, phoneNumber=perfil_phoneNumber, direccion=perfil_direccion)
            perfil.save()
            return render(request, "aplicacion/perfil.html")
    else:
        miForm = PerfilForm()
    return render(request, "aplicacion/perfilForm.html", {"form": miForm} )

# --------------- Compra ------------------------
@login_required
def compra(request):
    contexto = { 'compra': Compra.objects.all().order_by("id") }
    return render(request, "aplicacion/compra.html", contexto)

@login_required
def compraCreate(request):
    if request.method == "POST":
        miForm = CompraForm(request.POST)
        if miForm.is_valid():
            compra_producto = miForm.cleaned_data.get("producto")
            compra_codigo = miForm.cleaned_data.get("codigo")
            compra_cantidad = miForm.cleaned_data.get("cantidad")
            compra = Compra(producto=compra_producto, codigo=compra_codigo, cantidad=compra_cantidad)
            compra.save()
            
            contexto = {'compra': Compra.objects.all().order_by("id")}
            return render(request, "aplicacion/compra.html", contexto)
    else:
        miForm = CompraForm()
    return render(request, "aplicacion/compraForm.html", {"form": miForm} )

class CompraUpdate(LoginRequiredMixin, UpdateView):
    model = Compra
    fields = ["cantidad"]
    success_url = reverse_lazy("Compra")

@login_required
def compraDelete(request, id_compra):
    compras = Compra.objects.get(id=id_compra)
    compras.delete()
    return redirect(reverse_lazy('Compra'))

# --------------- Artista --------------------------

def artista(request):
    contexto = { 'artista': Artista.objects.all().order_by("nombreArtista") }
    return render(request, "aplicacion/artista.html", contexto)

def artistaCreate(request):
    if request.method == "POST":
        miForm = ArtistaForm(request.POST)
        if miForm.is_valid():
            artista_nombreArtista = miForm.cleaned_data.get("nombreArtista")
            artista_descripcion = miForm.cleaned_data.get("descripcion")
            artista = Artista(nombreArtista=artista_nombreArtista, descripcion=artista_descripcion)
            artista.save()
            
            contexto = {'artista': Artista.objects.all().order_by("nombreArtista")}
            return render(request, "aplicacion/artista.html", contexto)
    else:
        miForm = ArtistaForm()
    return render(request, "aplicacion/artistaForm.html", {"form": miForm} )

#--------------Fecha---------------------

def proximafecha(request):
    contexto = { 'proximafecha': ProximaFecha.objects.all().order_by("date") }
    return render(request, "aplicacion/proximafecha.html", contexto)


def proximafechaCreate(request):
    if request.method == "POST":
        miForm = ProximaFechaForm(request.POST, request.FILES)
        if miForm.is_valid():
            proximafecha_artista = miForm.cleaned_data.get("artista")
            proximafecha_date = miForm.cleaned_data.get("date")
            proximafecha_lugar = miForm.cleaned_data.get("lugar")
            proximafecha_descripcion = miForm.cleaned_data.get("descripcion")
            #proximafecha_img = miForm.cleaned_data.get["img"]
            proximafecha = ProximaFecha(artista=proximafecha_artista, date=proximafecha_date, lugar=proximafecha_lugar, descripcion=proximafecha_descripcion)
            proximafecha.save()
            
            img = ProximaFecha.objects.get().img.url
            request.session["concierto"] = img
            
            contexto = {'proximafecha': ProximaFecha.objects.all().order_by("date")}
            return render(request, "aplicacion/proximafecha.html", contexto)
    else:
        miForm = ProximaFechaForm()
    return render(request, "aplicacion/proximafechaForm.html", {"form": miForm} )


# -------------- Acerca de mi ------------
def acerca(request):
    return render(request, "aplicacion/acerca.html")



#------------ Buscador en Bd --------------

def buscar(request):
    return render(request, "aplicacion/buscar.html")

def encontrarArtista(request):
    if request.GET["buscar"]:
        patron = request.GET["buscar"]
        artista = Artista.objects.filter(nombreArtista__icontains=patron)
        contexto = {"artista": artista}
        return render(request, "aplicacion/artista.html", contexto)
    
    contexto = { 'artista': Artista.objects.all() }
    return render(request, "aplicacion/artista.html", contexto)

#----------- Log In, Log Out, Authentication, Registration ------

def login_request(request):
    if request.method == "POST":
        usuario = request.POST['username']
        clave = request.POST['password']
        user = authenticate(request, username=usuario, password=clave)
        if user is not None:
            login(request, user)
            
            #---- Avatar
            try:
                avatar = Avatar.objects.get(user=request.user.id).imagen.url
            except:
                avatar = "/media/avatares/default.png"
            finally:
                request.session["avatar"] = avatar
            #Fin Avatar
            
            return render(request, "aplicacion/home.html")
        else:
            return redirect(reverse_lazy('Login'))
            
    else:
        miForm = AuthenticationForm()
    return render(request, "aplicacion/login.html", {"form": miForm} )

def register(request):
    if request.method == "POST":
        miForm = RegistroForm(request.POST)
        
        if miForm.is_valid():
            usuario = miForm.cleaned_data.get("username")
            miForm.save()
            return redirect(reverse_lazy('home'))
            
    else:
        miForm = RegistroForm()
        
    return render(request, "aplicacion/registro.html", {"form": miForm} )


#-------------- Error 405--------------

def method_not_allowed(request, *args, **kwargs):
    return HttpResponseNotAllowed(['GET'], context="This view only allow GET request")
    
#--------Edicion de Perfil, Cambio Clave, Avatar---------
@login_required
def EditPerfil(request):
    
    usuario = request.user
    
    if request.method == "POST":
        miForm = UserEditForm(request.POST)
        
        if miForm.is_valid():
            user = User.objects.get(username=usuario)
            
            user.email = miForm.cleaned_data.get("email")
            user.first_name = miForm.cleaned_data.get("first_name")
            user.last_name = miForm.cleaned_data.get("last_name")
            user.save()
            return redirect(reverse_lazy('home'))
            
    else:
        miForm = UserEditForm(instance=usuario)
        
    return render(request, "aplicacion/editarPerfil.html", {"form": miForm} )

class CambiarClave(LoginRequiredMixin, PasswordChangeView):
    template_name = "aplicacion/cambiar_clave.html"
    success_url = reverse_lazy("home")
    
@login_required
def agregarAvatar(request):
    if request.method == "POST":
        miForm = AvatarForm(request.POST, request.FILES)
        
        if miForm.is_valid():
            usuario = User.objects.get(username=request.user)
          #---------Borrar avalar Viejo ------------ 
            avatarViejo = Avatar.objects.filter(user=usuario)
            if len(avatarViejo) > 0:
                for i in range(len(avatarViejo)):
                    avatarViejo[i].delete()
          #---------Fin Borrar avalar Viejo ------------  
            avatar = Avatar(user=usuario, imagen=miForm.cleaned_data["imagen"])
            avatar.save()
            imagen = Avatar.objects.get(user=usuario).imagen.url
            request.session["avatar"] = imagen
            return redirect(reverse_lazy('home'))
            
    else:
        miForm = AvatarForm()
        
    return render(request, "aplicacion/agregarAvatar.html", {"form": miForm} )