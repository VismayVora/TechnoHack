from rest_framework import serializers
from .models import Guardian, MyUser, Location, AuditForm, CheckIn


class RegisterSerializer(serializers.ModelSerializer):
	password=serializers.CharField(max_length=32,min_length=8,write_only = True)
	
	class Meta:
		model = MyUser
		fields = ['email','password','first_name','last_name','phone_no','address']
		
	def validate(self,attrs):
		phone_no = attrs.get('phone_no',' ')
		if not phone_no:
			raise serializers.ValidationError('Phone number is compulsory')
		return attrs
		
	def create(self,validated_data):
		return MyUser.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):
	password=serializers.CharField(max_length=32,min_length=8,write_only = True)
	
	class Meta:
		model = MyUser
		fields = ['phone_no','password']
        
	def validate(self,attrs):
		phone_no = attrs.get('phone_no',' ')
		if not phone_no:
			raise serializers.ValidationError('Phone number is compulsory')
		return attrs

class GuardianSerializer(serializers.ModelSerializer):
	owner = serializers.ReadOnlyField(source='owner.name')

	class Meta:
		model = Guardian
		fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):

	class Meta:
		model = Location
		fields = '__all__'

class AuditFormSerializer(serializers.ModelSerializer):
	author = serializers.ReadOnlyField(source='author.name')

	class Meta:
		model = AuditForm
		fields = '__all__'
    
class CheckInSerializer(serializers.ModelSerializer):
	author = serializers.ReadOnlyField(source='author.name')

	class Meta:
		model = CheckIn
		fields = '__all__'
		