from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('login', views.autenticar, name='Autentication'),
	path('', views.inicio, name='inicio'),
	path('logout', auth_views.logout, {'next_page': '/'}, name='logout'),
	path('agregarusuario', views.agregarusuario, name='agregarusuario'),
	path('usuarios', views.gestionarusuarios, name= 'gestionarusuarios'),
]