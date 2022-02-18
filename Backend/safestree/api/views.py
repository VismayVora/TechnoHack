import datetime
from django.contrib.auth import authenticate,login

from .models import MyUser,Guardian
from .serializers import RegisterSerializer, LoginSerializer, GuardianSerializer
from rest_framework import viewsets,permissions
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response

import requests

class RegisterAPI(GenericAPIView):
	
	serializer_class = RegisterSerializer
	
	def post(self,request,*args,**kwargs):
		data = request.data
		serializer = self.serializer_class(data=data)
		serializer.is_valid(raise_exception = True)
		user = serializer.save()
		
		return Response(serializer.data
		,status=status.HTTP_201_CREATED)


class LoginAPI(GenericAPIView):
	
	serializer_class = LoginSerializer
	
	def post(self,request,*args,**kwargs ):
		phone_no = request.data.get('phone_no',None)
		password = request.data.get('password',None)
		user = authenticate(phone_no=phone_no, password = password)
		if user :
			login(request,user)
			serializer = self.serializer_class(user)
			return Response({'first_name' : user.first_name},status = status.HTTP_200_OK)
		return Response('Invalid Credentials',status = status.HTTP_404_NOT_FOUND)
        
@api_view(('POST',))
def logout(self, request):
    logout(request)
    data = {'success': 'Sucessfully logged out'}
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(('POST',))
def news(self):
    url = ('https://newsapi.org/v2/everything?'
    'q=women+safety&'
    'searchln=description'
    f'from={datetime.date.today()}&'
    'sortBy=popularity&'
    'apiKey=c476157b8a084a4b8bdf8a1a8dd2a7a7')
    response = requests.get(url)
    return Response(response)
