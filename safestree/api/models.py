from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.forms import BooleanField
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token
from django.contrib.auth.base_user import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator

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
	points = models.IntegerField(default = 0,validators=[MinValueValidator(0), MaxValueValidator(5)])
	stars = models.IntegerField(default = 0,validators=[MinValueValidator(0), MaxValueValidator(5000)])
	
	USERNAME_FIELD = 'phone_no'
	REQUIRED_FIELDS = ['first_name',]
	
	objects = MyUserManager()
	
	def __str__(self):
		return self.first_name

	def star(self):
		if self.points >= 1000 & self.points<2000 :
			self.stars = 1
		elif self.points >= 2000 & self.points<3000 :
			self.stars = 2
		elif self.points >= 3000 & self.points<4000 :
			self.stars = 3
		elif self.points >= 4000 & self.points<5000 :
			self.stars = 4
		elif self.points >= 5000:
			self.stars = 5
		else:
			pass
		return self.stars

class Guardian(models.Model):
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='MyUser', on_delete=models.CASCADE)
	favourite = models.BooleanField()
	name = models.CharField(max_length=100)
	relation = models.CharField(max_length=100)
	phone_no = PhoneNumberField(unique = True)
	favourite = models.BooleanField(default = False)

class Location(models.Model):
	title = models.CharField(max_length=255,blank = True)
	latitude = models.FloatField()
	longitude = models.FloatField()
	safety_score = models.FloatField(default = 0)

	def __str__(self):
		return f'{self.latitude,self.longitude}'

	def get_score(self):
		reviews = AuditForm.objects.filter(location = self)
		count = 1
		for review in reviews:
			self.safety_score += review.score
			count += 1
		self.safety_score /= count
		return self.safety_score

class AuditForm(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='author', on_delete=models.CASCADE)
	location = models.ForeignKey(Location,on_delete=models.CASCADE)
	lighting = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
	openness = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
	visibility = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
	people = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
	security = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
	walk_path = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
	public_transport = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
	public_usage = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
	feeling = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
	score = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

	def __str__(self):
		return f'{self.location} - {self.score}'

class CheckIn(models.Model):
	logger = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='logger', on_delete=models.CASCADE)
	note = models.TextField(max_length=300)
	created_at = models.DateField(auto_now_add=True)
