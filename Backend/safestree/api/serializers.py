from rest_framework import serializers
from .models import Guardian, MyUser


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
    

		