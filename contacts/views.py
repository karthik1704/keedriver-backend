from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import permissions

from .models import contact
from.serializers import *

class ContactCreateView(CreateAPIView):

    # def post(self,request):
    #     new_contacts=contact(name= request.data ["name"],Email =request.data["Email"],Phone = request.data["Phone"],Message= request.data["Message"] )

    #     new_contacts.save()
    #     return Response(new_contacts)
    
    
    serializer_class=ContactSerializers
    permission_classes= {
        permissions.AllowAny
    }