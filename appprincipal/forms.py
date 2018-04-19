
#aqui se almacenan los formularios, creados a partir de los modelos

from django import forms
from .models import Programa
from .models import Curso
from .models import Profile
from django.contrib.auth.models import User


class ProgramaForm(forms.ModelForm):
	class Meta:
		model = Programa
		fields = '__all__'    
class CursoForm(forms.ModelForm):
	class Meta:
		model = Curso
		fields = '__all__'

class UserForm(forms.ModelForm):
	class Meta:
		password=forms.PasswordInput()
		model = User
		fields = ('first_name', 'username', 'password', 'email',)

class TipoForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('tipo',)