from django.shortcuts import render

from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend


from .models import Customer, Driver, MyUser
from .serializers import CustomerSerializer, DriverSerializer, MyUserSerializer, PasswordChangeSerializer
# Create your views here.

class MyUserViewset(viewsets.ModelViewSet):
    
    queryset = MyUser.objects.all().order_by('-date_joined')
    serializer_class = MyUserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_staff', 'is_driver', 'is_customer']

class MyUserPasswordChange(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def post(self, request):
        serializer = PasswordChangeSerializer(context={'request':request}, data=request.data)
        if serializer.is_valid():
            id=serializer.validated_data['new_password']
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CustomerViewset(viewsets.ModelViewSet):
    
    queryset = Customer.objects.all().order_by('-date_joined')
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class DriverViewset(viewsets.ModelViewSet):
    
    queryset = Driver.objects.all().order_by('-date_joined')
    serializer_class = DriverSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
