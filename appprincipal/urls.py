from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('login', views.autenticar, name='Autentication'),
	path('', views.inicio, name='inicio'),
	path('logout', auth_views.logout, {'next_page': '/'}, name='logout'),	
	path('usuarios', views.gestionarusuarios, name= 'gestionarusuarios'),
	path('usuarios/', views.gestionarusuarios, name= 'gestionarusuarios'),

	path('usuarios/new', views.agregarusuario, name='agregarusuario'),
	path('usuarios/<pk>', views.detalleUsuario, name='crudUsuario'),
	path('programas/', views.gestionarprogramas, name='gestionarprogramas'),
	path('programas/new', views.agregarprograma, name='agregarprograma'),
	path('programas/editar/<codigo>', views.editarPrograma, name='editarprograma'),
	path('programas/eliminar/<codigo>', views.eliminarPrograma, name='eliminarprograma'),
	path('programas/ver/<codigo>', views.verPrograma, name='verprograma')

]