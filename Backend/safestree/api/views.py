from django.contrib.auth import authenticate,login

from .models import MyUser,Guardian
from .serializers import RegisterSerializer, LoginSerializer, GuardianSerializer
from rest_framework import viewsets,permissions
from rest_framework.decorators import action,api_view
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response

from .whatsapp import send_message
from django.http import JsonResponse

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
        
@action(methods=['POST', ], detail=False)
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

@api_view(['POST'])
def sharelocation(self,request):
	location_link = request.data['link']
	favourites_list = []
	favourites = Guardian.objects.filter(owner=self.request.user)
	favourites_list.append(favourites)
	for favourite in favourites_list:
		message = f"Hello {favourite.name}, {favourite.owner} has started location sharing with you. Click on this link to track the location: {location_link}"
		send_message(request,favourite,message)
		
	return JsonResponse({"Message": "The message has been sent to the favourite guardians!"})

@api_view(['POST'])
def sos_alert(self,request):
	location_link = request.data['link']
	guardians_list = []
	guardians = Guardian.objects.filter(owner=self.request.user)
	guardians_list.append(guardians)
	for guardian in guardians_list:
		message = f"Hello {guardian.name}, {guardian.owner} is in trouble and has raised an SOS!!. Click on this link to track the location: {location_link}"
		send_message(request,guardian,message)
		
	return JsonResponse({"Message": "The message has been sent to the favourite guardians!"})

