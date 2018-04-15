from django.shortcuts import render, redirect
from .models import UsuarioPropio as User
from django.contrib.auth import authenticate, login

# Create your views here.

def autenticar(request):
	
	if(request.method == 'POST'):
		action = request.POST.get('action', None)
		username = request.POST.get('username', None)
		password = request.POST.get('password', None)
		tipo = request.POST.get('tipo', None)

		if(action == 'signup'):
			user = User.objects.create_user(username=username, password=password, tipo=tipo) 
			user.save()
			
		elif(action == 'login'):
			user = authenticate(username=username, password=password)
			login(request, user)
			
		return redirect('/')
	return render(request, 'login.html', {})
	
def inicio(request):
	return render(request, 'inicio.html', {})