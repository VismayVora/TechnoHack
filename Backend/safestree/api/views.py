import datetime
from django.contrib.auth import authenticate,login

from .models import MyUser,Guardian, Location, AuditForm
from .serializers import LocationSerializer, RegisterSerializer, LoginSerializer, GuardianSerializer, AuditFormSerializer
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

class GuardianDetails(viewsets.ModelViewSet):
	queryset = Guardian.objects.all()
	serializer_class = GuardianSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Guardian.objects.filter(owner=self.request.user)
	
	def perform_create(self,serializer):
		serializer.save(owner = self.request.user)
	
	def update(self, request, *args, **kwargs):
		kwargs['partial'] = True
		return super().update(request, *args, **kwargs)

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

class LocationAPI(GenericAPIView):
	serializer_class = LocationSerializer
	permission_classes = [permissions.IsAuthenticated]
	queryset = Location.objects.all()

	def post(self,request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid(raise_exception=True):
			serializer.save()
		return Response(serializer.data)

class AuditFormAPI(GenericAPIView):
	serializer_class = AuditFormSerializer
	permission_classes = [permissions.IsAuthenticated]
	queryset = AuditForm.objects.all()

	def post(self,request):
		score = 0
		score += request.data['lighting']
		score += request.data['openness']
		score += request.data['visibility']
		score += request.data['people']
		score += request.data['security']
		score += request.data['walk_path']
		score += request.data['public_transport']
		score += request.data['public_usage']
		score += request.data['feeling']
		score /= 9
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid(raise_exception=True):
			serializer.save(author=request.user,score = score)
			loc_id = request.data['location']
			location = Location.objects.get(id = loc_id)
			location.get_score()
			location.save()
			request.user.points += 50
			request.user.star()
			request.user.save()
		return Response(serializer.data)