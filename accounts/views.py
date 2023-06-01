from django.shortcuts import render

from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import UpdateAPIView
from django_filters.rest_framework import DjangoFilterBackend

import calendar
import datetime
from .models import Customer, Driver, MyUser
from .serializers import CustomerSerializer, DriverSerializer, MyUserSerializer, PasswordChangeSerializer
# Create your views here.

class MyUserViewset(viewsets.ModelViewSet):
    
    queryset = MyUser.objects.all().order_by('-date_joined')
    serializer_class = MyUserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_staff', 'is_driver', 'is_customer']
    ordering_fields = ["created_at", ]
    search_fields = ['first_name', 'last_name','phone',  'username']

class MyUserPasswordChange(UpdateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = PasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class CustomerViewset(viewsets.ModelViewSet):
    
    queryset = Customer.objects.all().order_by('-date_joined')
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    ordering_fields = ["created_at", ]
    search_fields = ['first_name', 'last_name','phone',  ] 

    @action(detail=False, methods=['get'], url_path="chart")
    def get_customer_chart(self, request):
        range = request.data.range
        if range == 'LAST30':
            pass

        if range =='LAST6':
            pass

        if range=="CUSTOM":
            pass
        
            
        today = datetime.date.today()
        year = today.year
        users = Customer.objects.filter(date_joined__year=year)
        months = []
        for user in users:
            months.append(user.date_joined.date().month)
        months = list(set(months))
        months.sort()
        data = []
        for month in months:
            data.append({
                'month': calendar.month_name[month],
                'count': Customer.objects.filter(date_joined__month=month).count()
            })
        return Response(data, status=status.HTTP_200_OK)

       

class DriverViewset(viewsets.ModelViewSet):
    
    queryset = Driver.objects.all().order_by('-date_joined')
    serializer_class = DriverSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    ordering_fields = ["created_at", ]
    search_fields = ['first_name', 'last_name','phone',  ]
    
    @action(detail=False, methods=['get'], url_path="chart")
    def get_driver_chart(self, request):
       
        users = Driver.objects.filter(date_joined__year=2023)
        months = []
        for user in users:
            months.append(user.date_joined.date().month)
        months = list(set(months))
        months.sort()
        data = []
        for month in months:
            data.append({
                'month': calendar.month_name[month],
                'count': Driver.objects.filter(date_joined__month=month).count()
            })
        return Response(data, status=status.HTTP_200_OK)
