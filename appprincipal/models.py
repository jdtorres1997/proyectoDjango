from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
	user=models.OneToOneField(User, on_delete=models.CASCADE)
	tipo = models.TextField(max_length=500, blank=True)

	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
		if(created):
			Profile.objects.create(user=instance)

	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()

class Programa(models.Model):
	codigo = models.CharField(max_length=255, primary_key=True)
	nombre_programa = models.CharField(max_length=255)
	escuela = models.CharField(max_length=255)
	numero_semestres =  models.CharField(max_length=255)
	numero_creditos_graduacion = models.CharField(max_length=255)

	def __str__(self): 
		return self.nombre

	class Meta:
		ordering = ('codigo',)
    
class Curso(models.Model):
	codigo=models.CharField(max_length=10, primary_key=True)
	nombre=models.CharField(max_length=40)
	creditos=models.IntegerField()
	horas_clase_magistral=models.IntegerField()
	horas_estudio_independiente=models.IntegerField()
	tipo_curso=models.CharField(max_length=20)
	validable=models.CharField(max_length=2) #Solo se acepta si o no
	habilitable=models.CharField(max_length=2) #Solo se acepta si o no
	programa=models.CharField(max_length=20) #debe cambiarse por llave foranea
	semestre=models.IntegerField()
