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
from .forms import UserForm
from .forms import TipoForm
from .models import Profile

class Factory:
	def crearFormulario(self, tipo, request=None):
		if(tipo == 'user'):
			if(request != None):
				return UserForm(request.POST)
			else:
				return UserForm()
		elif(tipo == 'tipo'):
			if(request != None):
				return TipoForm(request.POST)
			else:
				return TipoForm()
		elif(tipo == 'programa'):
			if(request != None):
				return ProgramaForm(request.POST)
			else:
				return ProgramaForm()
		elif(tipo == 'curso'):
			if(request != None):
				return CursoForm(request.POST)
			else:
				return CursoForm()
			
# Create your views here.
def autenticar(request):
	template = loader.get_template('login.html')
	if(request.user.is_authenticated):
		return redirect('/')
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
	return HttpResponse(template.render(context, request))

def inicio(request):
	if(request.user.is_authenticated):
			usuario = request.user
			form = UserForm(instance=usuario)
			formT = TipoForm(instance=usuario.profile)
			template = loader.get_template('verPerfil.html')
			context = {
				'texto' : "Información de mi perfil:",
				'form' : form,
				'tipo' : formT
			}
			return HttpResponse(template.render(context, request))
	else:
		return redirect('/login')

#------------------Crud usuarios--------------
def agregarusuario(request):
	factory = Factory()
	if(request.user.is_authenticated):
		if(request.user.profile.tipo == 'admin'):
			if(request.method == 'POST'):
				form = factory.crearFormulario('user', request)
				formT = factory.crearFormulario('tipo', request)
				username = request.POST.get('username', None)
				name = request.POST.get('first_name', None)
				password = request.POST.get('password', None)
				email = request.POST.get('email', None)
				tipo = request.POST.get('tipo', None)
				if form.is_valid():
					user = User.objects.create_user(username=username, password=password, email=email, first_name=name)
					user.profile.tipo = tipo
					user.save()
					return HttpResponseRedirect('/usuarios')
			else:
				form = factory.crearFormulario('user')
				formT = factory.crearFormulario('tipo')
			template = loader.get_template('agregarUsuario2.html')
			context = {
				'form' : form,
				'tipo' : formT, 
			}
			form.fields['password'] = forms.CharField(widget=forms.PasswordInput)
			return HttpResponse(template.render(context, request))
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
			usuario = get_object_or_404(User, pk=pk)
			form = UserForm(instance=usuario)
			formT = TipoForm(instance=usuario.profile)
			template = loader.get_template('verPerfil.html')
			context = {
				'texto' : "Perfil del usuario:",
				'form' : form,
				'tipo' : formT
			}
			return HttpResponse(template.render(context, request))
		else:
			return redirect('/')
	else:
		return redirect('/')

def modificarUsuario(request, pk):
	if(request.user.is_authenticated):
		if(request.user.profile.tipo == 'admin'):
			usuario = get_object_or_404(User, pk=pk)
			if(request.method == 'POST'):
				form = UserForm(request.POST, instance=usuario)
				form.fields['password'].widget = forms.HiddenInput()
				formT = TipoForm(request.POST, instance=usuario)
				username = request.POST.get('username', None)
				name = request.POST.get('first_name', None)
				email = request.POST.get('email', None)
				tipo = request.POST.get('tipo', None)
				if form.is_valid() and formT.is_valid():
					if(username != ""):
						usuario.username = username
					if(tipo != ""):
						usuario.profile.tipo = tipo
					if(name != ""):
						usuario.last_name = name
					if(email != ""):
						usuario.email = email
					usuario.save()
					return HttpResponseRedirect('/usuarios')
				else:
					template = loader.get_template('modificarUsuario.html')
					context = {
						'form' : form,
						'tipo' : formT,
					}
					return HttpResponse(template.render(context, request))
			else:
				
				form = UserForm(instance=usuario)
				form.fields['password'].widget = forms.HiddenInput()
				formT = TipoForm(instance=usuario.profile)
				template = loader.get_template('modificarUsuario.html')
				context = { #Diccionario que se le pasa al HTML
					'form': form,
					'tipo' : formT,
				}
				return HttpResponse(template.render(context, request))
		else:
			return redirect('/')
	else:
		return redirect('/')


#-------------Crud programas------------------
def agregarprograma(request):
	factory = Factory()
	if(request.user.is_authenticated):
		if(request.user.profile.tipo == 'decano'):
			template = loader.get_template('agregarPrograma.html')
			profileQuery = Profile.objects.filter(tipo="director")
			qs = User.objects.filter(profile__in=profileQuery).order_by('id')
			form = factory.crearFormulario('programa', request)
			form.fields['director'].queryset=qs;
			if request.method == 'POST':
				if form.is_valid():
					programa = form.save()
					programa.save()
					return HttpResponseRedirect('/programas')
			else:
				form = factory.crearFormulario('programa')
				form.fields['director'].queryset=qs;
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
		elif(request.user.profile.tipo == 'director'):
			programas = Programa.objects.filter(director_id=request.user.pk)#-------------Buscame----------------
			template = loader.get_template('programas.html') #Modificar template para gestion del director
			context = { #Diccionario que se le pasa al HTML
				'programas': programas
			}
			return HttpResponse(template.render(context, request))
		else:
			return redirect('/') # sin permisos
	else:
		return redirect('/login')

def editarPrograma(request, codigo): #Falta revisar html
	if(request.user.is_authenticated):
		programa = Programa.objects.get(codigo=codigo)
		if((request.user.profile.tipo == 'decano') or (request.user.id == programa.director_id)):
			profileQuery = Profile.objects.filter(tipo="director")
			qs = User.objects.filter(profile__in=profileQuery).order_by('id')
			if request.method == 'POST':
				#Actualiza
				#programa = Programa.objects.get(codigo=codigo)
				form = ProgramaForm(request.POST, instance=programa)
				form.fields['director'].queryset=qs;
				form.fields['codigo'].widget = forms.HiddenInput()
				if form.is_valid():
					form.save()
					return HttpResponseRedirect('/programas')
				else:
					form.fields['codigo'].widget = forms.HiddenInput()
					form.fields['director'].queryset=qs;
					template = loader.get_template('editarPrograma.html')
					context = {
					'form' : form,
					'pr' : programa
					}
					return HttpResponse(template.render(context, request))
			else:
				#programa =  Programa.objects.get(codigo=codigo)
				form = ProgramaForm(instance=programa)
				form.fields['codigo'].widget = forms.HiddenInput()
				form.fields['director'].queryset=qs;
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
		programa = Programa.objects.get(codigo=codigo)
		if(request.user.profile.tipo == 'decano' or request.user.id == programa.director_id):
			if request.method == 'POST':
				respuesta = request.POST.get('opcion', None)
				if(respuesta=="si"):
					#programa = Programa.objects.get(codigo=codigo);
					programa.delete()
				return redirect('/programas')
			else:
				#Mostrar en eliminar/<pk>
				#programa =  Programa.objects.get(codigo=codigo)
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
		programa = Programa.objects.get(codigo=codigo)
		if(request.user.profile.tipo == 'decano' or request.user.id == programa.director_id):
			#Tabla a HTML
			#programa = Programa.objects.get(codigo=codigo)
			form = ProgramaForm(instance=programa)
			form.fields['director'].widget = forms.HiddenInput()
			template = loader.get_template('tabla.html')
			context = { #Diccionario que se le pasa al HTML
				'form' : form,
				'programa' : programa,
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
			try:
				programa = Programa.objects.get(director_id=request.user.id)
			except Programa.DoesNotExist:
				template = loader.get_template('index.html') #---------Buscame-------------
				context = { #Diccionario que se le pasa al HTML
					'error': "No tiene programa academico asignado",
				}
				return HttpResponse(template.render(context, request))
			cursos = Curso.objects.filter(programa_id=programa.codigo)
			template = loader.get_template('cursos.html')
			
			context = {
				'cursos' : cursos
			}
			return HttpResponse(template.render(context, request))
		elif(request.user.profile.tipo == 'profesor'):
			curso = Curso.objects.filter(docente_id=request.user.pk)
			template = loader.get_template('cursos.html') #Modificar template para gestion del director
			context = { #Diccionario que se le pasa al HTML
				'cursos': cursos
			}
			return HttpResponse(template.render(context, request))
		else:
			return redirect('/')
	else:
		return redirect('/')

def agregarCurso(request):
	factory = Factory()
	if(request.user.is_authenticated):
		if(request.user.profile.tipo == 'director'):
			if(request.method == 'POST'):
				form = factory.crearFormulario('curso', request)
				if form.is_valid():
					curso = form.save()
					curso.save()
					return HttpResponseRedirect('/cursos')
			else:
				form = factory.crearFormulario('curso')
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
		curso = Curso.objects.get(codigo=codigo)
		programa = Programa.objects.get(codigo=curso.programa_id)
		if((request.user.profile.tipo == 'director' and request.user.id == programa.director_id) or request.user.id == curso.docente_id):
			if(request.method == 'POST'):
				#curso = Curso.objects.get(codigo=codigo)
				form = CursoForm(data = request.POST or None , instance=curso)
				if form.is_valid():
					form.save()
					return HttpResponseRedirect('/cursos')
				else:
					template = loader.get_template('modificarCurso.html')
					context = {
						'form' : form,
						'pr' : programa
					}
					return HttpResponse(template.render(context, request))
			
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
		curso = Curso.objects.get(codigo=codigo)
		programa = Programa.objects.get(codigo=curso.programa_id)
		if(request.user.profile.tipo == 'director' and request.user.id == programa.director_id):
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
		curso = Curso.objects.get(codigo=codigo)
		programa = Programa.objects.get(codigo=curso.programa_id)
		if((request.user.profile.tipo == 'director' and request.user.id == programa.director_id) or request.user.id == curso.docente_id):
			return redirect('/cursos') #Cambiar-----------------------
		else:
			return redirect('/')
	else:
		return redirect('/')
