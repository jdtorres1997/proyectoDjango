#aqui se almacenan los formularios, credos a partir de los modelos

from django import forms
from .models import Programa


class ProgramaForm(forms.ModelForm):
	class Meta:
		model = Programa
		fields = '__all__'