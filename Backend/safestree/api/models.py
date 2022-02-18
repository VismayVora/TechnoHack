from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token
from django.contrib.auth.base_user import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField

class MyUserManager(BaseUserManager):
	def create_user(self,phone_no,password=None,**extra_fields):
		user = self.model(phone_no = phone_no, **extra_fields)
		if not password:
			password = 'user1234'
		user.set_password(password)
		user.save()
		return user
		
	def create_superuser(self,phone_no,password=None,**extra_fields):
		extra_fields.setdefault('is_superuser',True)
		extra_fields.setdefault('is_staff',True)
		user = self.create_user(phone_no,password,**extra_fields)
		user.save()
		return user

class MyUser(AbstractBaseUser,PermissionsMixin):
	email = models.EmailField(_('email address'),unique = True)
	first_name = models.CharField(max_length = 20)
	last_name = models.CharField(max_length = 20)
	phone_no = PhoneNumberField(unique = True)
	address = models.TextField(max_length =100, blank = True)
	is_staff = models.BooleanField(default = False)
	
	USERNAME_FIELD = 'phone_no'
	REQUIRED_FIELDS = ['first_name',]
	
	objects = MyUserManager()
	
	def __str__(self):
		return self.first_name

class Guardian(models.Model):
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='MyUser', on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	relation = models.CharField(max_length=100)
	phone_no = PhoneNumberField(unique = True)

