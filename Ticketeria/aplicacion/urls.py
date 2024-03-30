from django.urls import path, include
from .views import *

from django.contrib.auth.views import LogoutView

from django.conf.urls import handler400

handler400 = 'aplicacion.views.method_not_allowed'

urlpatterns = [
    path('', home, name="home"),
    #url, funcion, index
    
    # ----------- perfil -------------
    path('perfil', perfil, name="Perfil"),
    path('perfilCreate', perfilCreate, name="PerfilCreate"),
    
    # ----------- compra -------------
    path('compra', compra, name="Compra"),
    path('compraCreate', compraCreate, name="CompraCreate"),
    path('compraUpdate/<int:pk>', CompraUpdate.as_view(), name="CompraUpdate"),
    path('compraDelete/<id_compra>', compraDelete, name="CompraDelete"),
    
    # ----------- artista -------------
    path('artista', artista, name="Artista"),
    path('ArtistaCreate', artistaCreate, name="ArtistaCreate"),
    
    # ----------- fechas -------------
    path('proximafecha', proximafecha, name="Proximafecha"),
    path('ProximaFechaCreate', proximafechaCreate, name="ProximaFechaCreate"),
    path('proximafechacomprar/<id_proximafecha>', proximafechaComprar, name="ProximafechaComprar"),
    
    
    # ----------- Otras paginas ---------
    path('acerca', acerca, name="Acerca"),
    
    
    #----------- Busqueda -------------
    path('Buscar', buscar, name="buscar"),
    path('encontrarArtista', encontrarArtista, name="encontrarArtista"),
    
    #----------- Log In, Log Out, Registration ------
    path('login', login_request, name="Login"),
    path('logout', LogoutView.as_view(template_name="aplicacion/logout.html"), name="logout"),
    path('registrar', register, name="Registrar"),
    
    #--------Edicion de Perfil, Cambio Clave, Avatar---------
    
    path('editPerfil', EditPerfil, name="EditarPerfil"),
    path('<int:pk>/password/', CambiarClave.as_view(), name="cambiar_clave"),
    path('agregarAvatar', agregarAvatar, name="agregarAvatar"),
]   