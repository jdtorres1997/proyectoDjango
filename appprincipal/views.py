from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# Create your views here.

def autenticar(request):
	
	if(request.method == 'POST'):
		
		username = request.POST.get('username', None)
		password = request.POST.get('password', None)
		user = authenticate(username=username, password=password)
		login(request, user)	
		return redirect('/')

	return render(request, 'login.html', {})
	
def inicio(request):
	return render(request, 'inicio.html', {})

def agregarusuario(request):

	if(request.method == 'POST'):
		username = request.POST.get('username', None)
		password = request.POST.get('password', None)
		tipo = request.POST.get('tipo', None)
		user = User.objects.create_user(username=username, password=password)
		user.profile.tipo = tipo #Añadido
		user.save() #Añadido
		return redirect('/')

	return render(request, 'agregarUsuario.html', {})