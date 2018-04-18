from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ProgramaForm
from .models import Programa
from django import forms
from .models import Curso
from .forms import CursoForm

# Create your views here.
def autenticar(request):
	template = loader.get_template('login.html')
	if(request.method == 'POST'):
		username = request.POST.get('username', None)
		password = request.POST.get('password', None)
		user = authenticate(username=username, password=password)#Agregar login con correo
		if(user != None):
			login(request, user)
			return redirect('/')
		else:
			context = {
				'datosIncorrectos' : True
			}
			return HttpResponse(template.render(context, request))
	context = {
		'datosIncorrectos' : False
	}
	if(request.user.is_authenticated):
		return redirect('/')
	return HttpResponse(template.render(context, request))

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

def agregarprograma(request):
	if(request.user.is_authenticated):
		if(request.user.profile.tipo == 'decano'):
			form = ProgramaForm(request.POST, request.FILES)
			if request.method == 'POST':
				if form.is_valid():
					programa = form.save()
					programa.save()
					return HttpResponseRedirect('/programas')
			else:
				form = ProgramaForm()
			template = loader.get_template('agregarPrograma.html')
			context = {
				'form' : form
			}
			return HttpResponse(template.render(context, request))
		else:
			return redirect('/') # sin permisos
	else:
		return redirect('/login')

def gestionarprogramas(request):

	if(request.user.is_authenticated):
		if(request.user.profile.tipo == 'decano'):
			programas = Programa.objects.order_by('codigo')
			template = loader.get_template('programas.html')
			context = { #Diccionario que se le pasa al HTML
				'programas': programas
			}
			return HttpResponse(template.render(context, request))
		else:
			return redirect('/') # sin permisos
	else:
		return redirect('/login')

def editarPrograma(request, codigo):

	if(request.user.is_authenticated):
		if(request.user.profile.tipo == 'decano'):
			if request.method == 'POST':
				#Actualiza
				programa = Programa.objects.get(codigo=codigo);
				form = ProgramaForm(request.POST, instance=programa)
				form.fields['codigo'].widget = forms.HiddenInput()
				if form.is_valid():
					form.save()
					return HttpResponseRedirect('/programas')
				else:
					#form = ProgramaForm()
					template = loader.get_template('editarPrograma.html')
					context = {
					'form' : form,
					'pr' : programa
					}
					return HttpResponse(template.render(context, request))
			else:
				#Mostrar en editar/<pk>
				programa =  Programa.objects.get(codigo=codigo)
				form = ProgramaForm(instance=programa)
				#form.fields["codigo"].initial= programa.codigo
				#form.fields['codigo'].widget.attrs['readonly'] = True # text input
				form.fields['codigo'].widget = forms.HiddenInput()
				#form.fields["nombre_programa"].initial= programa.nombre_programa
				#form.fields["escuela"].initial= programa.escuela
				#form.fields["numero_semestres"].initial= programa.numero_semestres
				#form.fields["numero_creditos_graduacion"].initial= programa.numero_creditos_graduacion
				template = loader.get_template('editarPrograma.html')
				context = { #Diccionario que se le pasa al HTML
				'form': form,
				'pr' : programa
				}
				return HttpResponse(template.render(context, request))
		else:
			return redirect('/') # sin permisos
	else:
		return redirect('/login')

def eliminarPrograma(request, codigo):
	if(request.user.is_authenticated):
		if(request.user.profile.tipo == 'decano'):
			if request.method == 'POST':
				respuesta = request.POST.get('opcion', None)
				if(respuesta=="si"):
					programa = Programa.objects.get(codigo=codigo);
					programa.delete()
				return redirect('/programas')
			else:
				#Mostrar en eliminar/<pk>
				programa =  Programa.objects.get(codigo=codigo)
				template = loader.get_template('confirmar.html')
				context = { #Diccionario que se le pasa al HTML
				'pr' : programa
				}
				return HttpResponse(template.render(context, request))
		else:
			return redirect('/') # sin permisos
	else:
		return redirect('/login')

def verPrograma(request,codigo):
	if(request.user.is_authenticated):
		if(request.user.profile.tipo == 'decano'):
			#Tabla a HTML
			programa = Programa.objects.get(codigo=codigo)
			form = ProgramaForm(instance=programa)
			template = loader.get_template('tabla.html')
			context = { #Diccionario que se le pasa al HTML
				'form' : form
			}
			return HttpResponse(template.render(context, request))
		else:
			return redirect('/') #sin permisos
	else:
		return redirect('/login')

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
