
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

	def clean(self):
		magistral = self.cleaned_data['horas_clase_magistral']
		independiente = self.cleaned_data['horas_estudio_independiente']
		cred = self.cleaned_data['creditos']
		print(magistral)
		print(independiente)
		print(cred)
		if(magistral + independiente != cred*3):
			raise forms.ValidationError("Verifique los creditos y las horas de trabajo individual y magistral")

class UserForm(forms.ModelForm):
	class Meta:
		password=forms.PasswordInput()
		model = User
		fields = ('first_name', 'username', 'password', 'email',)

class TipoForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('tipo',)