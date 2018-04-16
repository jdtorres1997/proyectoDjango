from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

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

				if(accion == "consultar"):
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
					
					usuario = get_object_or_404(User, pk=pk) #Saca un objeto que su pk sea igual a la ingresada
					template = loader.get_template('usuario.html') 
					context = {
						'usuario': usuario
					}
					return HttpResponse(template.render(context, request))

				elif(accion == "eliminar"):
					password = request.POST.get('password', None)
					user = User.objects.get(pk=pk)
					user.delete()

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
