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

'''
class Product(models.Model):
	nombre = models.CharField(max_length=255)
	descripcion = models.CharField(max_length=255)
	categoria = models.CharField(max_length=255)
	precio = models.DecimalField(max_digits=6, decimal_places=2)
	imagen = models.ImageField(blank=True)
	
	def __str__(self): 
		return self.nombre

	class Meta:
		ordering = ('id',)
		'''