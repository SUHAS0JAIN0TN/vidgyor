from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import UserManager
# Create your models here.

class User(AbstractBaseUser):
	email = models.EmailField(
		verbose_name='Email Field',
		max_length=255,
		unique=True
		)
	name=models.CharField(max_length=30)
	active = models.BooleanField(default=True)
	staff = models.BooleanField(default=False)
	admin = models.BooleanField(default=False)
	USERNAME_FIELD='email'
	REQUIRED_FIELDS=['name']

	def __str__(self):
		return self.email

	@property
	def is_admin(self):
		return self.admin
	
	@property
	def is_active(self):
		return self.active

	@property
	def is_staff(self):
		return self.staff
	

	objects=UserManager()


class vid(models.Model):
	title=models.CharField(max_length=20)
	description= models.CharField(max_length=40)
	tags=models.CharField(max_length=20)
	categories=models.CharField(max_length=20)
	thumbnail=models.FileField(upload_to='thumbnails')
	videos=models.FileField(upload_to='videos')