from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .models import Curso
from .forms import CursoForm
from django import forms


# Create your views here.

def autenticar(request):
	
	if(request.method == 'POST'):
		
		username = request.POST.get('username', None)
		password = request.POST.get('password', None)
		user = authenticate(username=username, password=password)#Agregar login con correo
		if(user != None):
			login(request, user)	
		return redirect('/')

	return render(request, 'login.html', {})	

def inicio(request):
	return render(request, 'inicio.html', {})

#------------------Crud usuarios--------------
def agregarusuario(request):

	if(request.user.is_authenticated):
		if(request.user.profile.tipo == 'admin'):
			if(request.method == 'POST'):

				username = request.POST.get('username', None)
				name = request.POST.get('name', None)
				password = request.POST.get('password', None)
				email = request.POST.get('email', None)
				tipo = request.POST.get('tipo', None)
				user = User.delete
				user = User.objects.create_user(username=username, password=password, email=email, last_name=name)
				user.profile.tipo = tipo #Añadido
				user.save() #Añadido
				return redirect('/')

			return render(request, 'agregarUsuario.html', {})
		else:
			return redirect('/')
	else:
		return redirect('/')

def gestionarusuarios(request):
	if(request.user.is_authenticated):
		if(request.user.profile.tipo == 'admin'):
			usuarios = User.objects.order_by('id')
			template = loader.get_template('usuarios.html')
			
			context = {
				'usuarios' : usuarios
			}
			return HttpResponse(template.render(context, request))
		else:
			return redirect('/')
	else:
		return redirect('/')
	
def detalleUsuario(request, pk):
	if(request.user.is_authenticated):
		if(request.user.profile.tipo == 'admin'):
			return redirect('/') #Cambiar-----------------------
		else:
			return redirect('/')
	else:
		return redirect('/')

def modificarUsuario(request, pk):
	if(request.user.is_authenticated):
		if(request.user.profile.tipo == 'admin'):
			if(request.method == 'POST'):
				
				username = request.POST.get('username', None)
				name = request.POST.get('name', None)
				password = request.POST.get('password', None)
				email = request.POST.get('email', None)
				tipo = request.POST.get('tipo', None)
				usuario = get_object_or_404(User, pk=pk)
				if(username != ""):
					usuario.username = username
				if(password != ""):
					usuario.password = password
				if(tipo != ""):
					usuario.profile.tipo = tipo
				if(name != ""):
					usuario.last_name = name
				if(email != ""):
					usuario.email = email
				usuario.save()
				return redirect('/usuarios')

			else:
				usuario = get_object_or_404(User, pk=pk) #Saca un objeto que su pk sea igual a la ingresada
				template = loader.get_template('modificarUsuario.html') 
				context = {
					'usuario': usuario
				}
				return HttpResponse(template.render(context, request))
		else:
			return redirect('/')
	else:
		return redirect('/')

def eliminarUsuario(request, pk):
	if(request.user.is_authenticated):
		if(request.user.profile.tipo == 'admin'):
			if(request.method == 'POST'):
				opcion = request.POST.get('opcion', None)
				if(opcion == 'si'):
					user = User.objects.get(pk=pk)
					user.delete()
				
				return redirect('/usuarios')
			else:
				return redirect('/usuarios')#Mostrar el template para eliminar
		else:
			return redirect('/')
	else:
		return redirect('/')


#-------------------Crud cursos---------------------


def gestionarCursos(request):
	if(request.user.is_authenticated):
		if(request.user.profile.tipo == 'director'):
			cursos = Curso.objects.order_by('codigo')
			template = loader.get_template('cursos.html')
			
			context = {
				'cursos' : cursos
			}
			return HttpResponse(template.render(context, request))
		else:
			return redirect('/')
	else:
		return redirect('/')

def agregarCurso(request):
	if(request.user.is_authenticated):
		if(request.user.profile.tipo == 'director'):
			if(request.method == 'POST'):
				form = CursoForm(request.POST)
				if form.is_valid():
					curso = form.save()
					curso.save()
					return HttpResponseRedirect('/cursos')
			
			form = CursoForm()

			template = loader.get_template('agregarCurso.html')
	
			context = {
				'form' : form
			}
			return HttpResponse(template.render(context, request))
		else:
			return redirect('/')
	else:
		return redirect('/')

def modificarCurso(request, codigo):
	if(request.user.is_authenticated):
		if(request.user.profile.tipo == 'director'):
			if(request.method == 'POST'):
				curso = Curso.objects.get(codigo=codigo)
				form = CursoForm(data = request.POST or None , instance=curso)
				if form.is_valid():
					form.save()
					return HttpResponseRedirect('/cursos')
			
			curso = Curso.objects.get(codigo=codigo)
			form = CursoForm(instance = curso)
			form.fields['codigo'].widget = forms.HiddenInput()
			template = loader.get_template('modificarCurso.html')
	
			context = {
				'form' : form
			}
			return HttpResponse(template.render(context, request))
		else:
			return redirect('/')
	else:
		return redirect('/')

def eliminarCurso(request, codigo):
	if(request.user.is_authenticated):
		if(request.user.profile.tipo == 'director'):
			if(request.method == 'POST'):
				opcion = request.POST.get('opcion', None)
				if(opcion == 'si'):
					curso = Curso.objects.get(codigo=codigo)
					curso.delete()
				return redirect('/cursos')
			else:
				return redirect('/cursos')#Mostrar el template para eliminar
		else:
			return redirect('/')
	else:
		return redirect('/')

def consultarCurso(request, codigo):
	if(request.user.is_authenticated):
		if(request.user.profile.tipo == 'director'):
			return redirect('/') #Cambiar-----------------------
		else:
			return redirect('/')
	else:
		return redirect('/')