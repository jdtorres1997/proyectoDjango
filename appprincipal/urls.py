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
	path('usuarios/consultar/<pk>', views.detalleUsuario, name='crudUsuario'),
	path('usuarios/editar/<pk>', views.modificarUsuario, name='crudUsuario'),
	path('usuarios/eliminar/<pk>', views.eliminarUsuario),
	path('cursos', views.gestionarCursos, name='gestionarcursos'),
	path('cursos/', views.gestionarCursos, name='gestionarcursos'),
	path('cursos/new', views.agregarCurso, name='agregarCurso'),
	path('cursos/consultar/<codigo>', views.consultarCurso),
	path('cursos/editar/<codigo>', views.modificarCurso),
	path('cursos/eliminar/<codigo>', views.eliminarCurso),
]