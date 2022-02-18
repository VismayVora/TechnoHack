from django.contrib.auth import authenticate,login

from .models import MyUser,Guardian
from .serializers import RegisterSerializer, LoginSerializer, GuardianSerializer
from rest_framework import viewsets,permissions
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response

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
