import datetime
from django.contrib.auth import authenticate,login
from django.conf import settings
from .models import CheckIn, MyUser,Guardian, Location, AuditForm

from .serializers import LocationSerializer, RegisterSerializer, LoginSerializer, GuardianSerializer, AuditFormSerializer, CheckInSerializer
from rest_framework import viewsets,permissions
from rest_framework.decorators import action,api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response

from .whatsapp import send_message
from django.http import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework import status
from twilio.rest import Client
import requests

def send_text(number,msg):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN )
    message = client.messages.create(body= f'{msg}',
        to =str(number),
        from_ ='+12346574691')
    return('success')

def call_me(number):
	client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN )
	call = client.calls.create(
                        twiml='<Response><Say>Ahoy, World!</Say></Response>',
                        to=str(number),
                        from_='+12346574691'
                    )
	return('success')

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

@api_view(('GET',))
def news(self):
    url = ('https://newsapi.org/v2/everything?'
    'q=women+safety&'
    'searchln=description'
    f'from={datetime.date.today()}&'
    'sortBy=popularity&'
    'apiKey=c476157b8a084a4b8bdf8a1a8dd2a7a7')
    response = requests.get(url)
    return Response(response.json())

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

@api_view(('POST',))
@permission_classes([permissions.IsAuthenticated])
def sharelocation(self):
	location_link = self.data['link']
	guardians = Guardian.objects.filter(owner=self.user)#, favourite = True)
	for guardian in guardians:
		msg = f"Hello {guardian.name}, {guardian.owner} has started location sharing with you. Click on this link to track the location: {location_link}"
		send_message(self,guardian,msg)
		k = send_text(guardian.phone_no,msg)
	
	return Response({'success':"The message has been sent to the favourite guardians!"})

@api_view(('POST',))
@permission_classes([permissions.IsAuthenticated])
def sos_alert(self):
	location_link = self.data['link']
	guardians = Guardian.objects.filter(owner=self.user)
	for guardian in guardians:
		msg = f"Hello {guardian.name}, {guardian.owner} is in trouble and has raised an SOS!!. Click on this link to track the location: {location_link}"
		send_message(self,guardian,msg)
		k = send_text(guardian.phone_no,msg)
	return Response({'success':"The message has been sent to guardians!"})

@api_view(('GET',))
@permission_classes([permissions.IsAuthenticated])
def fakecall(self):
	user = self.user
	call = call_me(user.phone_no)
	return Response({'success':"Fake call has been generated!"})

@api_view(('POST',))
def nearby_search(keywords,latitude,longitude):
	url = f"https://atlas.mapmyindia.com/api/places/nearby/json?keywords={keywords}&refLocation={latitude,longitude}"
	payload={}
	headers ={
		'Authorization': 'bearer 7455992d-57e7-4a4a-8b54-7a433ea4dc1f'
		}
		
	response = requests.request("GET", url, headers=headers, data=payload)
	print(response.text)


class CheckInAPI(viewsets.ModelViewSet):
	serializer_class = CheckInSerializer
	permission_classes = [permissions.IsAuthenticated]
	queryset = CheckIn.objects.all()

	def get_queryset(self,phone_no):
		return CheckIn.objects.filter(logger__phone_no=phone_no)
	
	def perform_create(self,serializer):
		serializer.save(logger = self.request.user)
	
	#def update(self, request, *args, **kwargs):
		#kwargs['partial'] = True
		#return super().update(request, *args, **kwargs)

