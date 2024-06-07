from rest_framework import generics

from rest_framework import permissions
from.models import FAQ
from .serializers import FAQSerializer
from rest_framework.generics import ListAPIView 
from .serializers import FAQSerializer


class FAQCreateView(ListAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [permissions.AllowAny]

 