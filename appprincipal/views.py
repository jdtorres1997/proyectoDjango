from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ProgramaForm
from .models import Programa
from django import forms

# Create your views here.
def autenticar(request):
	
	if(request.method == 'POST'):
		
		username = request.POST.get('username', None)
		password = request.POST.get('password', None)
		user = authenticate(username=username, password=password)
		if(user != None):
			login(request, user)	
		return redirect('/')

	return render(request, 'login.html', {})	

def inicio(request):
	return render(request, 'inicio.html', {})


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
			if(request.method == 'POST'):
				accion = request.POST.get('accion', None)

				if(accion == "modificar"):
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
					'''
					usuario = get_object_or_404(User, pk=pk) #Saca un objeto que su pk sea igual a la ingresada
					template = loader.get_template('usuario.html') 
					context = {
						'usuario': usuario
					}
					return HttpResponse(template.render(context, request))
					'''

				elif(accion == "eliminar"):
					password = request.POST.get('password', None)
					user = User.objects.get(pk=pk)
					user.delete()

					#return redirect('/usuarios')
				return redirect('/usuarios')

			else:
				usuario = get_object_or_404(User, pk=pk) #Saca un objeto que su pk sea igual a la ingresada
				template = loader.get_template('usuario.html') 
				context = {
					'usuario': usuario
				}
				return HttpResponse(template.render(context, request))
		else:
			return redirect('/')
	else:
		return redirect('/')



def agregarprograma(request):

	if request.method == 'POST':
		form = ProgramaForm(request.POST, request.FILES)
		if form.is_valid():
			programa = form.save()
			programa.save()
			return HttpResponseRedirect('/programas')
	form = ProgramaForm()
	template = loader.get_template('agregarPrograma.html')
	context = {
		'form' : form
	}
	return HttpResponse(template.render(context, request))


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
			return redirect('/nopermisos')
	else:
		return redirect('/login')

def editarPrograma(request, codigo):

	if(request.user.is_authenticated):
		if(request.user.profile.tipo == 'decano'):
			if request.method == 'POST':
				#Actualiza
				programa = Programa.objects.get(codigo=codigo);
				form = ProgramaForm(request.POST, instance=programa)
				if form.is_valid():
					form.save()
					return HttpResponseRedirect('/programas')
				else:
					#form = ProgramaForm()
					template = loader.get_template('editarPrograma.html')
					context = {
					'form' : form
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
			return redirect('/nopermisos')
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
			return redirect('/nopermisos')
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
			return redirect('/nopermisos')
	else:
		return redirect('/login')