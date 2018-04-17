
#aqui se almacenan los formularios, credos a partir de los modelos

from django import forms
from .models import Programa
from .models import Curso

class ProgramaForm(forms.ModelForm):
	class Meta:
		model = Programa
		fields = '__all__'
    
class CursoForm(forms.ModelForm):
	class Meta:
		model = Curso
		fields = '__all__'