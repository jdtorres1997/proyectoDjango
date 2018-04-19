from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.conf.urls import include
from material.frontend import urls as frontend_urls
from appprincipal.views import DirectorAutocomplete

urlpatterns = [
    url(
        r'^director-autocomplete/$',
        DirectorAutocomplete.as_view(),
        name='director-autocomplete',
    ),
	url(r'', include(frontend_urls)),
	path('login', views.autenticar, name='Autentication'),
	path('', views.inicio, name='inicio'),
	path('logout', auth_views.logout, {'next_page': '/'}, name='logout'),	
	path('usuarios', views.gestionarusuarios, name= 'gestionarusuarios'),
	path('usuarios/', views.gestionarusuarios, name= 'gestionarusuarios'),
	path('usuarios/new', views.agregarusuario, name='agregarusuario'),
	path('usuarios/consultar/<pk>', views.detalleUsuario, name='crudUsuario'),
	path('usuarios/editar/<pk>', views.modificarUsuario, name='crudUsuario'),
	path('usuarios/eliminar/<pk>', views.eliminarUsuario),
	path('programas/', views.gestionarprogramas, name='gestionarprogramas'),
	path('programas/new', views.agregarprograma, name='agregarprograma'),
	path('programas/editar/<codigo>', views.editarPrograma, name='editarprograma'),
	path('programas/eliminar/<codigo>', views.eliminarPrograma, name='eliminarprograma'),
	path('programas/ver/<codigo>', views.verPrograma, name='verprograma'),
	path('cursos', views.gestionarCursos, name='gestionarcursos'),
	path('cursos/', views.gestionarCursos, name='gestionarcursos'),
	path('cursos/new', views.agregarCurso, name='agregarCurso'),
	path('cursos/consultar/<codigo>', views.consultarCurso),
	path('cursos/editar/<codigo>', views.modificarCurso),
	path('cursos/eliminar/<codigo>', views.eliminarCurso),
]